from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .connect_device import ConnectDeviceProfile, ConnectMainDevice, ConnectSubDevice


class WasherProfile(ConnectDeviceProfile):
    """Washer Profile."""

    _LOCATION_MAP = {"MAIN": "main", "MINI": "mini"}

    def __init__(self, profile: dict[str, Any]):
        super().__init__(profile, use_sub_profile_only=True)
        _location_properties = {}
        for profile_property in profile.get("property", []):
            location_name = profile_property.get("location", {}).get("locationName")
            if location_name in self._LOCATION_MAP.keys():
                attr_key = self._LOCATION_MAP[location_name]
                _sub_profile = WasherSubProfile(profile, location_name)
                setattr(self, attr_key, _sub_profile)
                _location_properties[attr_key] = _sub_profile.properties
        self._location_properties = _location_properties
        self._PROFILE = WasherSubProfile._PROFILE

    @property
    def notification(self) -> dict | None:
        for location in self._LOCATION_MAP.values():
            if _notification := self.get_sub_profile(location).notification:
                return _notification
        return None


class WasherSubProfile(ConnectDeviceProfile):
    """Washer Profile Sub."""

    _RESOURCE_MAP = {
        "runState": "run_state",
        "operation": "operation",
        "remoteControlEnable": "remote_control_enable",
        "timer": "timer",
        "detergent": "detergent",
    }

    _PROFILE = {
        "runState": {"currentState": "current_state"},
        "operation": {
            "washerOperationMode": "washer_operation_mode",
        },
        "remoteControlEnable": {"remoteControlEnabled": "remote_control_enabled"},
        "timer": {
            "remainHour": "remain_hour",
            "remainMinute": "remain_minute",
            "totalHour": "total_hour",
            "totalMinute": "total_minute",
            "relativeHourToStop": "relative_hour_to_stop",
            "relativeMinuteToStop": "relative_minute_to_stop",
            "relativeHourToStart": "relative_hour_to_start",
            "relativeMinuteToStart": "relative_minute_to_start",
        },
        "detergent": {"detergentSetting": "detergent_setting"},
    }

    def __init__(self, profile: dict[str, Any], location_name: str = None):
        self._location_name = location_name
        super().__init__(profile)

    def generate_properties(self, property: list[dict[str, Any]] | dict[str, Any]) -> None:
        """Get properties."""
        if isinstance(property, list):
            for location_property in property:
                if location_property.get("location", {}).get("locationName") != self._location_name:
                    continue
                super().generate_properties(location_property)
        else:
            super().generate_properties(property)


class WasherSubDevice(ConnectSubDevice):
    """Washer Device Sub."""

    def __init__(
        self,
        profiles: WasherSubProfile,
        thinq_api: ThinQApi,
        device_id: str,
        device_type: str,
        model_name: str,
        alias: str,
        reportable: bool,
        location_name: str = None,
        single_unit: bool = False,
    ):
        super().__init__(profiles, location_name, thinq_api, device_id, device_type, model_name, alias, reportable)

    @property
    def profiles(self) -> WasherSubProfile:
        return self._profiles

    @property
    def remain_time(self) -> dict:
        return {"hour": self.get_status("remain_hour"), "minute": self.get_status("remain_minute")}

    @property
    def total_time(self) -> dict:
        return {"hour": self.get_status("total_hour"), "minute": self.get_status("total_minute")}

    @property
    def relative_time_to_stop(self) -> dict:
        return {
            "hour": self.get_status("relative_hour_to_stop"),
            "minute": self.get_status("relative_minute_to_stop"),
        }

    @property
    def relative_time_to_start(self) -> dict:
        return {
            "hour": self.get_status("relative_hour_to_start"),
            "minute": self.get_status("relative_minute_to_start"),
        }

    def _set_status(self, status: dict | list, is_updated: bool = False) -> None:
        if isinstance(status, list):
            super()._set_status(status, is_updated)
        else:
            super(ConnectSubDevice, self)._set_status(status, is_updated)

    async def set_washer_operation_mode(self, mode: str) -> ThinQApiResponse:
        payload = self.profiles.get_enum_attribute_payload("washer_operation_mode", mode)
        return await self._do_attribute_command({"location": {"locationName": self._location_name}, **payload})

    async def set_relative_hour_to_start(self, hour: str) -> ThinQApiResponse:
        payload = self.profiles.get_range_attribute_payload("relative_hour_to_start", hour)
        return await self._do_attribute_command({"location": {"locationName": self._location_name}, **payload})

    async def set_relative_hour_to_stop(self, hour: str) -> ThinQApiResponse:
        payload = self.profiles.get_range_attribute_payload("relative_hour_to_stop", hour)
        return await self._do_attribute_command({"location": {"locationName": self._location_name}, **payload})


class WasherDevice(ConnectMainDevice):
    """Washer Property."""

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
        self._sub_devices: dict[str, WasherSubDevice] = {}
        super().__init__(
            thinq_api=thinq_api,
            device_id=device_id,
            device_type=device_type,
            model_name=model_name,
            alias=alias,
            reportable=reportable,
            profiles=WasherProfile(profile=profile),
            sub_device_type=WasherSubDevice,
        )

    @property
    def profiles(self) -> WasherProfile:
        return self._profiles

    def get_sub_device(self, location_name: str) -> WasherSubDevice:
        return super().get_sub_device(location_name)
