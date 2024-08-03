import asyncio
from datetime import datetime
import re
import sys
import traceback

import aiohttp

from agptools.helpers import DATE, camel_case_split
from agptools.logs import logger

from syncmodels.crud import parse_duri
from syncmodels.definitions import (
    ORG_KEY,
    REG_PRIVATE_KEY,
    ID_KEY,
)

from syncmodels import __version__


# from swarmtube.logic.swarmtube import (
#     SkipWave,
#     RetryWave,
# )


log = logger(__file__)


class OrionInjector:
    """
    Inject data into Orion using async http.
    """

    MAPPER = None
    EXCLUDE = set(["id", "type"])
    HEADER_KEYS = set(["fiware-service", "fiware-servicepath"])
    FULL_EXCLUDE = EXCLUDE.union(HEADER_KEYS)
    TYPES = {
        "ts": "timestamp",
        "date": "timestamp",
        "location": "geo:point",
        str: "string",
        float: "float",
        int: "integer",
    }
    TIMEOUT_INFO = aiohttp.ClientTimeout(
        total=None,
        # total timeout (time consists connection establishment for a new connection
        # or waiting for a free connection from a pool if pool connection limits are exceeded)
        # default value is 5 minutes, set to `None` or `0` for unlimited timeout
        sock_connect=15,
        # Maximal number of seconds for connecting to a peer for a new connection,
        # not given from a pool. See also connect.
        sock_read=15,
        # Maximal number of seconds for reading a portion of data from a peer
    )
    RETRY = 15

    HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": f"OrionInjector/{__version__}",
        # "Accept": "*/*",
        # "Accept-Encoding": "gzip, deflate, br",
        # additional headers for the FIWARE item
        # "fiware-service": "fs_ccoc",
        # "fiware-servicepath": "/beacons/traces",
    }

    # TARGET_URL = "https://orion.ccoc.spec-cibernos.com/v2/entities"
    SERVICE_PATH = ""  # Need to be overridden by the user or use default pattern generation

    def __init__(self, target_url, service, service_path):
        self.target_url = target_url
        self.service = service
        self.service_path = service_path
        self.methods = [
            (
                "patch",
                self.target_url
                + "/v2/entities/{id}/attrs?options=append,keyValues",
                self.FULL_EXCLUDE,
            ),
            (
                "post",
                self.target_url + "/v2/entities?options=append,keyValues",
                [],
            ),
        ]

    def get_service_path(self):
        "Generate service path from class name, removing common prefixes"
        name = self.service_path or self.__class__.__name__

        for ban in "Orion", "Particle", "Sync", "Tube":
            name = name.replace(ban, "")

        tokens = [""] + camel_case_split(name)
        name = "/".join(tokens).lower()
        return name

    def _guess_type(self, key, value):
        "Guess type of a key-value pair based on its value"
        type_ = self.TYPES.get(key)
        if type_ is None:
            if isinstance(value, str):
                x = DATE(value)
                if isinstance(x, datetime):
                    return "timestamp"
            # return default value of 'string'
            type_ = self.TYPES.get(value.__class__, "string")
        return type_

    def _to_fiware(self, data):
        """Create a json for Orion based on given data"""

        # "type" --> entity_type: i.e. beacons.traces
        _id = data.get(ID_KEY)
        if not _id:
            fquid = data.get(ORG_KEY) or data["_path"]

            _uri = parse_duri(fquid)
            entity_id = _uri[ID_KEY]

            # entity_id = tf(entity_id)
            # entity_id = esc(entity_id)
            data["id"] = entity_id
        # data["id"] = str(data[MONOTONIC_KEY])  # --> entity_id

        _ts = data.get("ts")
        if isinstance(_ts, int):
            # "ts": {
            #     "value": "2024-03-06 09:43:11",
            #     "type": "timestamp"
            # },
            date = DATE(_ts)
            # date = datetime.fromtimestamp(_ts / 1000000000)
            # data['ts'] = date.strfmt("%Y-%m-%d %H:%M:%S.%f %z")
            # data['ts'] = date.strftime("%Y-%m-%dT%H:%M:%S.%f")
            # data['ts'] = date.strftime("%Y-%m-%dT%H:%M:%S")  # --> entity_ts
            data["ts"] = {
                "type": "timestamp",
                "value": date.strftime("%Y-%m-%d %H:%M:%S"),  # --> entity_ts
            }
        try:
            data["location"] = "{lat},{lng}".format_map(data)
        except KeyError:
            pass

        data.setdefault(
            "type", self.get_service_path().replace("/", ".")[1:]
        )

        # check if a validation MAPPER is defined
        if self.MAPPER:
            item = self.MAPPER.pydantic(data)
            if item:
                data = item.model_dump(mode="json")
        else:
            # filter any private key when pydantic models are
            # not helping us, so if we need to publish a private
            # key, create a pydantic model that contains the key
            # and this purge will not be executed
            for key in list(data):
                if re.match(REG_PRIVATE_KEY, key):
                    data.pop(key)

        # get headers
        headers = {
            **self.HEADERS,
            "fiware-servicepath": data.pop("fiware-servicepath", "/test"),
        }
        # try to translate all regular existing fields
        for key in set(data.keys()).difference(self.FULL_EXCLUDE):
            value = data[key]

            if isinstance(value, dict) and not set(value.keys()).difference(
                ["value", "type"]
            ):
                pass
            else:
                data[key] = {
                    "value": value,
                    "type": self._guess_type(key, value),
                }
        return headers, data

    async def _push(self, session, data, headers):
        """
        # Update an entity
        # https://fiware-orion.readthedocs.io/en/1.10.0/user/update_action_types/index.html#update

        201: POST
        204: POST

        400: PATCH
        {'error': 'BadRequest', 'description': 'entity id specified in payload'}
        {'error': 'BadRequest', 'description': 'entity type specified in payload'}
        {'error': 'BadRequest', 'description': 'attribute must be a JSON object, unless keyValues option is used'}
        {'error': 'BadRequest', 'description': 'empty payload'}

        400: DELETE
        {'error': 'BadRequest', 'description': 'Orion accepts no payload for GET/DELETE requests. HTTP header Content-Type is thus forbidden'}


        404: PATCH
        {'error': 'NotFound', 'description': 'The requested entity has not been found. Check type and id'}
        {'orionError': {'code': '400',
                'reasonPhrase': 'Bad Request',
                'details': 'Service not found. Check your URL as probably it '
                           'is wrong.'}}

        422: POST
        {'error': 'Unprocessable', 'description': 'Already Exists'}
        {'error': 'Unprocessable', 'description': 'one or more of the attributes in the request do not exist: ['plate ]'}

        Example of headers

        headers = {
            "Content-Type": "application/json",
            "fiware-service": "fs_ccoc",
            "fiware-servicepath": "/test",
        }
        """
        for method, url, exclude in self.methods:
            method = getattr(session, method)
            url = url.format_map(data)
            _data = {k: v for k, v in data.items() if k not in exclude}
            async with method(
                url,
                json=_data,
                headers=headers,
            ) as response:
                if response.status < 300:
                    break
        return response

    async def _compute(self, edge, ekeys):
        """
        # TODO: looks like is a batch insertion! <-----

        Example
        {
        "actionType": "APPEND",
        "entities": [
            {
                "id": "TL1",
                "type": "totem.views",
                "ts": {
                    "value": "2024-03-06 09:43:11",
                    "type": "timestamp"
                },
                "conteo": {
                    "value": 9,
                    "type": "integer"
                },
                "component": {
                    "value": "C11 - TOTEMS",
                    "type": "string"
                },
                "place": {
                    "value": "LUCENTUM",
                    "type": "string"
                },
                "location": {
                    "type": "geo:point",
                    "value": "38.365156979723906,-0.438225677848391"
                }
            }
        ]
        }
        """
        assert len(ekeys) == 1, "Stream must have just 1 input tube"

        # returning None means that no data is really needed for synchronization
        # just advance the TubeSync wave mark
        for tube_name in ekeys:
            data = edge[tube_name]
            return await self.push(data)

    async def push(self, data, **context):
        """try to push data to Orion"""
        response = None
        headers, data = self._to_fiware(data)
        # update with context
        for key in self.HEADER_KEYS.intersection(context).difference(
            headers
        ):
            headers[key] = context[key]
        if data:
            for tries in range(0, self.RETRY):
                try:
                    async with aiohttp.ClientSession() as session:
                        response = await self._push(session, data, headers)
                        break

                except aiohttp.ClientError as why:
                    log.error(why)
                    log.error(
                        "".join(traceback.format_exception(*sys.exc_info()))
                    )
                log.warning("retry: %s: %s", tries, data)
                await asyncio.sleep(0.5)
            return response

            # if response:
            #     if response.status < 500:
            #         # not recoverable
            #         # we need to advance the wave cursor
            #         log.error(
            #             "%s: %s",
            #             response.status,
            #             data,
            #         )
            #         msg = {
            #             "reason": response.status,
            #             "url": self.target_url,
            #             "data": data,
            #         }
            #         raise SkipWave(msg)
            #     else:
            #         # need to retry later on
            #         # DO NOT advance the wave cursor
            #         log.error(
            #             "%s: %s",
            #             response.status,
            #             data,
            #         )
            #         msg = {
            #             "reason": response.status,
            #             "url": self.target_url,
            #             "data": data,
            #             "delay": 15,
            #         }
            #         raise RetryWave(msg)  #  retry in 15 secs
            # # need to retry later on
            # # DO NOT advance the wave cursor
            # log.error(
            #     "%s: %s",
            #     "Cannot connect to Orion",
            #     data,
            # )
            # msg = {
            #     "reason": "Cannot connect to Orion",
            #     "url": self.target_url,
            #     "data": data,
            #     "delay": 15,
            # }
            # raise RetryWave(msg)  #  retry in 15 secs
