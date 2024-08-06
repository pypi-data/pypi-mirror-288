import httpx
import asyncio
import logging
logger = logging.getLogger(__name__)


class AsyncHttpTransport:
    """
    AsyncHttpTransport class maintains a single instance of httpx.AsyncClient for all the AsyncShieldRestHttpClient instances.
    """
    _client: httpx.AsyncClient = None
    _lock = asyncio.Lock()

    _max_retries = 4
    _backoff_factor = 1
    _allowed_methods = ["GET", "POST", "PUT", "DELETE"]
    _status_forcelist = [500, 502, 503, 504]
    _connect_timeout_sec = 2.0
    _read_timeout_sec = 7.0
    """
    These are default settings that can be overridden by calling the setup method.
    """

    @staticmethod
    async def setup(**kwargs):
        """
        This optional method allows you to pass your own settings to be used by all the
        AsyncShieldRestHttpClient instances.
        :param kwargs:
            - client: Instance of httpx.AsyncClient
            - max_retries
            - backoff_factor
            - allowed_methods
            - status_forcelist
            - connect_timeout_sec
            - read_timeout_sec
        :return:
        """
        AsyncHttpTransport._client = kwargs.get('client', AsyncHttpTransport._client)
        AsyncHttpTransport._max_retries = kwargs.get('max_retries', AsyncHttpTransport._max_retries)
        AsyncHttpTransport._backoff_factor = kwargs.get('backoff_factor', AsyncHttpTransport._backoff_factor)
        AsyncHttpTransport._allowed_methods = kwargs.get('allowed_methods', AsyncHttpTransport._allowed_methods)
        AsyncHttpTransport._status_forcelist = kwargs.get('status_forcelist', AsyncHttpTransport._status_forcelist)
        AsyncHttpTransport._connect_timeout_sec = kwargs.get('connect_timeout_sec',
                                                             AsyncHttpTransport._connect_timeout_sec)
        AsyncHttpTransport._read_timeout_sec = kwargs.get('read_timeout_sec', AsyncHttpTransport._read_timeout_sec)

        await AsyncHttpTransport.create_default_client()

    @staticmethod
    async def get_client():
        if not AsyncHttpTransport._client:
            await AsyncHttpTransport.create_default_client()
        return AsyncHttpTransport._client

    @staticmethod
    async def create_default_client():
        async with AsyncHttpTransport._lock:
            if not AsyncHttpTransport._client:

                timeout = httpx.Timeout(
                    connect=AsyncHttpTransport._connect_timeout_sec,
                    read=AsyncHttpTransport._read_timeout_sec,
                    write=None,
                    pool=None
                )
                limits = httpx.Limits(max_keepalive_connections=50, max_connections=100)

                # Use RetryTransport instead of AsyncHTTPTransport
                transport = RetryTransport(
                    max_retries=AsyncHttpTransport._max_retries,
                    backoff_factor=AsyncHttpTransport._backoff_factor,
                    status_forcelist=AsyncHttpTransport._status_forcelist
                )

                AsyncHttpTransport._client = httpx.AsyncClient(
                    timeout=timeout,
                    transport=transport,
                    limits=limits
                )

    @staticmethod
    async def close():
        """
        Close the httpx AsyncClient.
        """
        if AsyncHttpTransport._client:
            await AsyncHttpTransport._client.aclose()
            AsyncHttpTransport._client = None


class RetryTransport(httpx.AsyncBaseTransport):
    def __init__(self, max_retries, backoff_factor, status_forcelist):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.status_forcelist = status_forcelist
        self._transport = httpx.AsyncHTTPTransport()

    async def handle_async_request(self, request):
        retries = 0
        response = None
        exception = None
        while retries < self.max_retries:
            try:
                response = await self._transport.handle_async_request(request)
                if response.status_code not in self.status_forcelist:
                    return response
            except httpx.RequestError as exc:
                exception = exc
            retries += 1
            await asyncio.sleep(self.backoff_factor * (2 ** (retries - 1)))

        # After max retries, raise the last encountered exception
        if response is None:
            logger.error(f"Max retries reached without a successful response getting this exception: {exception}")
            raise httpx.RequestError("Max retries reached without a successful response getting this exception: {exception}")

        return response
