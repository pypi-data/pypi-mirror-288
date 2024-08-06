from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .connect_device import ConnectDeviceProfile, ConnectMainDevice, ConnectSubDevice


class CooktopSubProfile(ConnectDeviceProfile):
    """Cooktop Profile."""

    _RESOURCE_MAP = {
        "cookingZone": "cooking_zone",
        "power": "power",
        "remoteControlEnable": "remote_control_enable",
        "timer": "timer",
    }

    _PROFILE = {
        "cookingZone": {
            "currentState": "current_state",
        },
        "power": {
            "powerLevel": "power_level",
        },
        "remoteControlEnable": {
            "remoteControlEnabled": "remote_control_enabled",
        },
        "timer": {
            "remainHour": "remain_hour",
            "remainMinute": "remain_minute",
        },
    }

    def __init__(self, profile: dict[str, Any], location_name: str):
        self._location_name = location_name
        super().__init__(profile)

    def generate_properties(self, property: dict[str, Any]) -> None:
        """Get properties."""
        for location_property in property:
            if location_property.get("location", {}).get("locationName") != self._location_name:
                continue
            super().generate_properties(location_property)


class CooktopProfile(ConnectDeviceProfile):
    """Cooktop Property."""

    _RESOURCE_MAP = {"operation": "operation"}

    _PROFILE = {"operation": {"operationMode": "operation_mode"}}

    _LOCATION_MAP = {
        "CENTER": "center",
        "CENTER_FRONT": "center_front",
        "CENTER_REAR": "center_rear",
        "LEFT_FRONT": "left_front",
        "LEFT_REAR": "left_rear",
        "RIGHT_FRONT": "right_front",
        "RIGHT_REAR": "right_rear",
        "BURNER_1": "burner_1",
        "BURNER_2": "burner_2",
        "BURNER_3": "burner_3",
        "BURNER_4": "burner_4",
        "BURNER_5": "burner_5",
        "BURNER_6": "burner_6",
        "BURNER_7": "burner_7",
        "BURNER_8": "burner_8",
        "INDUCTION_1": "induction_1",
        "INDUCTION_2": "induction_2",
        "SOUSVIDE_1": "sousvide_1",
    }

    def __init__(self, profile: dict[str, Any]):
        super().__init__(profile, use_extension_property=True)
        _location_properties = {}
        for profile_property in profile.get("property", []):
            location_name = profile_property.get("location", {}).get("locationName")
            if location_name in self._LOCATION_MAP.keys():
                attr_key = self._LOCATION_MAP[location_name]
                _sub_profile = CooktopSubProfile(profile, location_name)
                setattr(self, attr_key, _sub_profile)
                _location_properties[attr_key] = _sub_profile.properties
        self._location_properties = _location_properties


class CooktopSubDevice(ConnectSubDevice):
    """Cooktop Device Sub."""

    def __init__(
        self,
        profiles: CooktopSubProfile,
        location_name: str,
        thinq_api: ThinQApi,
        device_id: str,
        device_type: str,
        model_name: str,
        alias: str,
        reportable: bool,
    ):
        super().__init__(profiles, location_name, thinq_api, device_id, device_type, model_name, alias, reportable)

    @property
    def profiles(self) -> CooktopSubProfile:
        return self._profiles

    def _get_command_payload(self):
        return {
            "power": {"powerLevel": self.get_status("power_level")},
            "timer": {"remainHour": self.get_status("remain_hour"), "remainMinute": self.get_status("remain_minute")},
            "location": {"locationName": self.location_name},
        }

    async def _do_custom_range_attribute_command(self, attr_name: str, value: int) -> ThinQApiResponse:
        full_payload: dict[str, dict[str, int | str]] = self._get_command_payload()
        payload = self.profiles.get_range_attribute_payload(attr_name, value)
        for resource in payload.keys():
            full_payload[resource].update(payload[resource])
        return await self.thinq_api.async_post_device_control(device_id=self.device_id, payload=full_payload)

    async def set_power_level(self, value: int) -> ThinQApiResponse:
        return await self._do_custom_range_attribute_command("power_level", value)

    async def set_remain_hour(self, value: int) -> ThinQApiResponse:
        return await self._do_custom_range_attribute_command("remain_hour", value)

    async def set_remain_minute(self, value: int) -> ThinQApiResponse:
        return await self._do_custom_range_attribute_command("remain_minute", value)


class CooktopDevice(ConnectMainDevice):
    """Cooktop Property."""

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
        self._sub_devices: dict[str, CooktopSubDevice] = {}
        super().__init__(
            thinq_api=thinq_api,
            device_id=device_id,
            device_type=device_type,
            model_name=model_name,
            alias=alias,
            reportable=reportable,
            profiles=CooktopProfile(profile=profile),
            sub_device_type=CooktopSubDevice,
        )

    @property
    def profiles(self) -> CooktopProfile:
        return self._profiles

    def get_sub_device(self, location_name: str) -> CooktopSubDevice:
        return super().get_sub_device(location_name)

    async def set_operation_mode(self, mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("operation_mode", mode)

    async def set_power_level(self, location_name: str, value: int) -> ThinQApiResponse:
        if sub_device := self._sub_devices.get(location_name):
            return await sub_device.set_power_level(value)
        else:
            raise ValueError(f"Invalid location : {location_name}")

    async def set_remain_hour(self, location_name: str, value: int) -> ThinQApiResponse:
        if sub_device := self._sub_devices.get(location_name):
            return await sub_device.set_remain_hour(value)
        else:
            raise ValueError(f"Invalid location : {location_name}")

    async def set_remain_minute(self, location_name: str, value: int) -> ThinQApiResponse:
        if sub_device := self._sub_devices.get(location_name):
            return await sub_device.set_remain_minute(value)
        else:
            raise ValueError(f"Invalid location : {location_name}")
