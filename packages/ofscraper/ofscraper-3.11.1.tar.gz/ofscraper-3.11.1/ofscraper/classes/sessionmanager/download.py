import contextlib

import ofscraper.classes.sessionmanager.ofsession as ofsessionmanager
import ofscraper.classes.sessionmanager.sessionmanager as sessionManager
import ofscraper.actions.utils.globals as common_globals
import ofscraper.utils.constants as constants
from ofscraper.actions.utils.retries import get_download_req_retries
from ofscraper.classes.sessionmanager.sessionmanager import (
    AUTH,
    COOKIES,
    FORCED_NEW,
    HEADERS,
    SIGN,
    TOO_MANY,
)


class download_session(sessionManager.sessionManager):
    def __init__(
        self, sem_count=None, retries=None, wait_min=None, wait_max=None, log=None
    ) -> None:
        sem_count = sem_count or common_globals.sem
        retries = retries or get_download_req_retries()
        wait_min = wait_min or constants.getattr("OF_MIN_WAIT_API")
        wait_max = wait_max or constants.getattr("OF_MAX_WAIT_API")
        log = log or common_globals.log
        super().__init__(
            sem_count=sem_count, retries=retries, wait_min=wait_min, wait_max=wait_max, log=log
        )
    @contextlib.asynccontextmanager
    async def requests_async(self, *args, **kwargs):
        if not kwargs.get("actions"):
            actions = [SIGN, COOKIES, HEADERS]
            actions.append([FORCED_NEW]) if constants.getattr("API_FORCE_KEY") else None
            kwargs["actions"]= actions
        kwargs["exceptions"]= [TOO_MANY, AUTH]
        async with super().requests_async(
            *args,**kwargs
        ) as r:
            yield r


class cdm_session(sessionManager.sessionManager):
    def __init__(self, backend=None, sem_count=None) -> None:
        backend = backend or "httpx"
        sem_count = sem_count or common_globals.sem
        super().__init__(sem_count=sem_count, backend=backend)


class cdm_session_manual(ofsessionmanager.OFSessionManager):
    def __init__(self, backend=None, sem_count=None) -> None:
        backend = backend or "httpx"
        sem_count = sem_count or common_globals.sem
        super().__init__(sem_count=sem_count, backend=backend)
