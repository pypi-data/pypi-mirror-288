"""Support for LG ThinQ Connect API."""

from __future__ import annotations

import base64
import logging
import uuid
from typing import Any

from aiohttp import ClientResponse, ClientSession
from aiohttp.hdrs import METH_DELETE, METH_GET, METH_POST
from aiohttp.typedefs import StrOrURL

from .const import API_KEY
from .country import get_region_from_country

_LOGGER = logging.getLogger(__name__)


class ThinQApiResponse:
    """The class that represnets a response for LG ThinQ API request."""

    def __init__(
        self,
        success: bool,
        status: int,
        payload: dict,
    ):
        """Initialize response."""
        self.status = status
        self.message_id = payload.get("messageId")
        self.timestamp = payload.get("timestamp")
        self.error_message = None
        self.error_code = None
        self.body = payload.get("response")
        if not success:
            error = payload.get("error", {})
            self.error_message = error.get("message", "unknown error message")
            self.error_code = error.get("code", "unknown error code")
        _LOGGER.debug("ThinQApiResponse: %s", self)

    @property
    def status(self) -> int:
        """Returns http status code."""
        return self._status

    @status.setter
    def status(self, status: int):
        self._status = status

    @property
    def body(self) -> dict | None:
        """Returns the response body."""
        return self._body

    @body.setter
    def body(self, body: dict):
        self._body = body

    @property
    def message_id(self) -> str | None:
        """Returns the message id used when making the request."""
        return self._message_id

    @message_id.setter
    def message_id(self, message_id: str):
        self._message_id = message_id

    @property
    def timestamp(self) -> str | None:
        """Returns the timestamp."""
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: str):
        self._timestamp = timestamp

    @property
    def error_code(self) -> str | None:
        """Returns the error code defined by the ThinQ Connect API."""
        return self._error_code

    @error_code.setter
    def error_code(self, error_code: str):
        self._error_code = error_code

    @property
    def error_message(self) -> str | None:
        """Returns the error message defined by the ThinQ Connect API."""
        return self._error_message

    @error_message.setter
    def error_message(self, error_message: str):
        self._error_message = error_message

    def __str__(self) -> str:
        return (
            f"ThinQResponse ("
            f"status:{self._status}, "
            f"message_id:{self._message_id}, "
            f"timestamp:{self._timestamp}, "
            f"body:{self._body}, "
            f"error:{self.error_code},{self.error_message})"
        )


class ThinQApi:
    """The class for using LG ThinQ Connect API."""

    def __init__(
        self,
        session: ClientSession,
        access_token: str,
        country_code: str,
        client_id: str,
    ):
        """Initialize settings."""
        self._access_token = access_token
        self._client_id = client_id
        self._api_key = API_KEY
        self._session = session
        self._phase = "OP"
        self._country_code = country_code
        self._region_code = get_region_from_country(country_code)

    def __await__(self):
        yield from self.async_init().__await__()
        return self

    async def async_init(self):
        pass

    def set_log_level(self, level):
        numeric_level = getattr(logging, level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f"Invalid log level: {level}")
        _LOGGER.setLevel(numeric_level)

    def _get_url_from_endpoint(self, endpoint: str) -> str:
        """Returns the URL to connect from the given endpoint."""
        return f"https://api-{self._region_code.lower()}.lgthinq.com/{endpoint}"

    def _generate_headers(self, headers: dict = {}) -> dict:
        """Generate common headers for request."""
        return {
            "Authorization": f"Bearer {self._access_token}",
            "x-country": self._country_code,
            "x-message-id": self._generate_message_id(),
            "x-client-id": self._client_id,
            "x-api-key": self._api_key,
            "x-service-phase": self._phase,
            **headers,
        }

    async def _async_fetch(self, method: str, url: StrOrURL, **kwargs: Any) -> ClientResponse:
        headers: dict[str, Any] = kwargs.pop("headers", {})
        if self._session is None:
            self._session = ClientSession()
        return await self._session.request(
            method=method,
            url=url,
            **kwargs,
            headers=headers,
        )

    async def async_get_device_list(self, timeout: int | float = 15) -> ThinQApiResponse:
        return await self.async_request(method=METH_GET, endpoint="devices", timeout=timeout)

    async def async_get_device_profile(self, device_id: str, timeout: int | float = 15) -> ThinQApiResponse:
        return await self.async_request(
            method=METH_GET,
            endpoint=f"devices/{device_id}/profile",
            timeout=timeout,
        )

    async def async_get_device_status(self, device_id: str, timeout: int | float = 15) -> ThinQApiResponse:
        return await self.async_request(method=METH_GET, endpoint=f"devices/{device_id}/state", timeout=timeout)

    async def async_post_device_control(
        self, device_id: str, payload: Any, timeout: int | float = 15
    ) -> ThinQApiResponse:
        headers = {"x-conditional-control": "true"}
        return await self.async_request(
            method=METH_POST,
            endpoint=f"devices/{device_id}/control",
            json=payload,
            timeout=timeout,
            headers=headers,
        )

    async def async_post_client_register(self, payload: Any, timeout: int | float = 15) -> ThinQApiResponse:
        return await self.async_request(
            method=METH_POST,
            endpoint="client",
            json=payload,
            timeout=timeout,
        )

    async def async_delete_client_register(self, payload: Any, timeout: int | float = 15) -> ThinQApiResponse:
        return await self.async_request(
            method=METH_DELETE,
            endpoint="client",
            json=payload,
            timeout=timeout,
        )

    async def async_post_client_certificate(self, payload: Any, timeout: int | float = 15) -> ThinQApiResponse:
        return await self.async_request(
            method=METH_POST,
            endpoint="client/certificate",
            json=payload,
            timeout=timeout,
        )

    async def async_get_push_list(self, timeout: int | float = 15) -> ThinQApiResponse:
        return await self.async_request(
            method=METH_GET,
            endpoint="push",
            timeout=timeout,
        )

    async def async_post_push_subscribe(self, device_id: str, timeout: int | float = 15) -> ThinQApiResponse:
        return await self.async_request(
            method=METH_POST,
            endpoint=f"push/{device_id}/subscribe",
            timeout=timeout,
        )

    async def async_delete_push_subscribe(self, device_id: str, timeout: int | float = 15) -> ThinQApiResponse:
        return await self.async_request(
            method=METH_DELETE,
            endpoint=f"push/{device_id}/unsubscribe",
            timeout=timeout,
        )

    async def async_get_event_list(self, timeout: int | float = 15) -> ThinQApiResponse:
        return await self.async_request(
            method=METH_GET,
            endpoint="event",
            timeout=timeout,
        )

    async def async_post_event_subscribe(self, device_id: str, timeout: int | float = 15) -> ThinQApiResponse:
        """Subscribe to event notifications for the device."""
        return await self.async_request(
            method=METH_POST,
            endpoint=f"event/{device_id}/subscribe",
            json={"expire": {"unit": "HOUR", "timer": 4464}},
            timeout=timeout,
        )

    async def async_delete_event_subscribe(self, device_id: str, timeout: int | float = 15) -> ThinQApiResponse:
        """Unsubscribe to event notifications for the device."""
        return await self.async_request(
            method=METH_DELETE,
            endpoint=f"event/{device_id}/unsubscribe",
            timeout=timeout,
        )

    async def async_post_push_devices_list(self, timeout: int | float = 15) -> ThinQApiResponse:
        """Get the list of clients subscribed to push notifications for devices registered,unregistered, and alias updated."""
        return await self.async_request(
            method=METH_GET,
            endpoint="push/devices",
            timeout=timeout,
        )

    async def async_post_push_devices_subscribe(self, timeout: int | float = 15) -> ThinQApiResponse:
        """Subscribe to push notifications for devices registered,unregistered, and alias updated."""
        return await self.async_request(
            method=METH_POST,
            endpoint="push/devices",
            timeout=timeout,
        )

    async def async_delete_push_devices_subscribe(self, timeout: int | float = 15) -> ThinQApiResponse:
        """Unsubscribe to push notifications for devices registered,unregistered, and alias updated."""
        return await self.async_request(
            method=METH_DELETE,
            endpoint="push/devices",
            timeout=timeout,
        )

    async def async_get_route(self, timeout: int | float = 15) -> ThinQApiResponse:
        return await self.async_request(
            method=METH_GET,
            endpoint="route",
            timeout=timeout,
        )

    async def async_request(self, method: str, endpoint: str, **kwargs: Any) -> ThinQApiResponse:
        url = self._get_url_from_endpoint(endpoint)
        headers = self._generate_headers(kwargs.pop("headers", {}))
        _LOGGER.debug(
            "async_request. method=%s, headers=%s, url=%s, kwargs=%s",
            method,
            headers,
            url,
            kwargs,
        )
        async with await self._async_fetch(method=method, url=url, **kwargs, headers=headers) as response:
            return ThinQApiResponse(success=response.ok, status=response.status, payload=await response.json())

    def _generate_message_id(self) -> str:
        return base64.urlsafe_b64encode(uuid.uuid4().bytes)[:-2].decode("utf-8")
