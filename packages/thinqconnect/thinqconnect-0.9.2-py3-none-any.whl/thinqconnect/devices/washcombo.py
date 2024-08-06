from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .washer import WasherSubDevice, WasherSubProfile


class WashcomboDevice(WasherSubDevice):
    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, value: str):
        self._location = value

    @property
    def group_id(self) -> str:
        return self._group_id

    @group_id.setter
    def group_id(self, value: str):
        self._group_id = value

    async def set_washer_operation_mode(self, operation: str) -> ThinQApiResponse:
        payload = self.profiles.get_enum_attribute_payload("washer_operation_mode", operation)
        return await self._do_attribute_command({"location": {"locationName": self.location}, **payload})

    async def set_relative_hour_to_start(self, hour: int) -> ThinQApiResponse:
        payload = self.profiles.get_range_attribute_payload("relative_hour_to_start", hour)
        return await self._do_attribute_command({"location": {"locationName": self.location}, **payload})

    async def set_relative_hour_to_stop(self, hour: int) -> ThinQApiResponse:
        payload = self.profiles.get_range_attribute_payload("relative_hour_to_stop", hour)
        return await self._do_attribute_command({"location": {"locationName": self.location}, **payload})

    def __init__(
        self,
        thinq_api: ThinQApi,
        device_id: str,
        device_type: str,
        model_name: str,
        alias: str,
        group_id: str,
        reportable: bool,
        profile: dict[str, Any],
        location: str,
    ):
        super().__init__(
            profiles=WasherSubProfile(profile=profile, location_name=location),
            location_name=location,
            single_unit=True,
            thinq_api=thinq_api,
            device_id=device_id,
            device_type=device_type,
            model_name=model_name,
            alias=alias,
            reportable=reportable,
        )
        self.group_id = group_id
        self.location = location
