from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .connect_device import ConnectBaseDevice, ConnectDeviceProfile
from .dryer import DryerDevice, DryerProfile
from .washer import WasherSubDevice, WasherSubProfile


class WashTowerProfile(ConnectDeviceProfile):
    """Washer Profile."""

    _LOCATION_MAP = {"DRYER": "dryer", "WASHER": "washer"}

    def __init__(self, profile: dict[str, Any]):
        super().__init__(profile, use_sub_profile_only=True)
        _location_properties = {}
        for location_name, attr_key in self._LOCATION_MAP.items():
            _sub_profile = (
                WasherSubProfile(profile=profile.get("washer"))
                if location_name == "WASHER"
                else DryerProfile(profile=profile.get("dryer"))
            )
            setattr(self, attr_key, _sub_profile)
            _location_properties[attr_key] = _sub_profile.properties
        self._location_properties = _location_properties


class WasherDeviceSingle(WasherSubDevice):
    """Washtower Washer Single Device."""

    async def set_washer_operation_mode(self, operation: str) -> ThinQApiResponse:
        payload = self.profiles.get_enum_attribute_payload("washer_operation_mode", operation)
        return await self._do_attribute_command({"washer": {**payload}})

    async def set_relative_hour_to_start(self, hour: int) -> ThinQApiResponse:
        payload = self.profiles.get_range_attribute_payload("relative_hour_to_start", hour)
        return await self._do_attribute_command({"washer": {**payload}})

    async def set_relative_hour_to_stop(self, hour: int) -> ThinQApiResponse:
        payload = self.profiles.get_range_attribute_payload("relative_hour_to_stop", hour)
        return await self._do_attribute_command({"washer": {**payload}})


class DryerDeviceSingle(DryerDevice):
    """Washtower Dryer Single Device."""

    async def set_dryer_operation_mode(self, operation: str) -> ThinQApiResponse:
        payload = self.profiles.get_enum_attribute_payload("dryer_operation_mode", operation)
        return await self._do_attribute_command({"dryer": {**payload}})

    async def set_relative_time_to_start(self, hour: int) -> ThinQApiResponse:
        payload = self.profiles.get_range_attribute_payload("relative_hour_to_start", hour)
        return await self._do_attribute_command({"dryer": {**payload}})

    async def set_relative_time_to_stop(self, hour: int) -> ThinQApiResponse:
        payload = self.profiles.get_range_attribute_payload("relative_hour_to_stop", hour)
        return await self._do_attribute_command({"dryer": {**payload}})


class WashtowerDevice(ConnectBaseDevice):
    def __init__(
        self,
        thinq_api: ThinQApi,
        device_id: str,
        device_type: str,
        model_name: str,
        alias: str,
        reportable: bool,
        profile: dict[str, Any],
    ):
        super().__init__(
            thinq_api=thinq_api,
            device_id=device_id,
            device_type=device_type,
            model_name=model_name,
            alias=alias,
            reportable=reportable,
            profiles=WashTowerProfile(profile=profile),
        )
        self._sub_devices: dict[str, WasherDeviceSingle | DryerDeviceSingle] = {}
        self.dryer = DryerDeviceSingle(
            thinq_api=thinq_api,
            device_id=device_id,
            device_type=device_type,
            model_name=model_name,
            alias=alias,
            reportable=reportable,
            profile=profile.get("dryer"),
        )
        self.washer = WasherDeviceSingle(
            single_unit=True,
            thinq_api=thinq_api,
            device_id=device_id,
            device_type=device_type,
            model_name=model_name,
            alias=alias,
            reportable=reportable,
            profiles=self.profiles.get_sub_profile("washer"),
        )
        self._sub_devices["dryer"] = self.dryer
        self._sub_devices["washer"] = self.washer

    def set_status(self, status: dict) -> None:
        super().set_status(status)
        for device_type, sub_device in self._sub_devices.items():
            sub_device.set_status(status.get(device_type))

    def update_status(self, status: dict) -> None:
        super().update_status(status)
        for device_type, sub_device in self._sub_devices.items():
            sub_device.update_status(status.get(device_type))

    def get_sub_device(self, location_name: str) -> DryerDeviceSingle | WasherDeviceSingle:
        return super().get_sub_device(location_name)
