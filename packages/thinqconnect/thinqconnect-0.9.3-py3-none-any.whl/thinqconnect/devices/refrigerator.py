from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .connect_device import READABLE_VALUES, WRITABLE_VALUES, ConnectDeviceProfile, ConnectMainDevice, ConnectSubDevice


class RefrigeratorSubProfile(ConnectDeviceProfile):
    """Refrigerator Profile."""

    _RESOURCE_MAP = {
        "doorStatus": "door_status",
        "temperature": "temperature",
    }
    _PROFILE = {
        "doorStatus": {
            "doorState": "door_state",
        },
        "temperature": {
            "targetTemperature": "target_temperature",
            "unit": "temperature_unit",
        },
    }
    _CUSTOM_RESOURCES = ["doorStatus", "temperature"]

    def __init__(self, profile: dict[str, Any], location_name: str):
        self._location_name = location_name
        super().__init__(profile)

    def _generate_custom_resource_properties(
        self, resource_key: str, resource_property: dict | list, props: dict[str, str]
    ) -> tuple[list[str], list[str]]:
        # pylint: disable=unused-argument
        readable_props = []
        writable_props = []
        if resource_key not in self._PROFILE.keys():
            return readable_props, writable_props

        for _location_property in resource_property:
            if _location_property["locationName"] != self._location_name:
                continue
            for _property_key in self._PROFILE[resource_key].keys():
                attr_name = self._PROFILE[resource_key][_property_key]
                prop = self._get_properties(_location_property, _property_key)
                self._set_prop_attr(attr_name, prop)
                if prop[READABLE_VALUES]:
                    readable_props.append(attr_name)
                if prop[WRITABLE_VALUES]:
                    writable_props.append(attr_name)

        return readable_props, writable_props


class RefrigeratorProfile(ConnectDeviceProfile):
    """Refrigerator Profile."""

    _RESOURCE_MAP = {
        "powerSave": "power_save",
        "ecoFriendly": "eco_friendly",
        "sabbath": "sabbath",
        "refrigeration": "refrigeration",
        "waterFilterInfo": "water_filter_info",
    }
    _PROFILE = {
        "powerSave": {
            "powerSaveEnabled": "power_save_enabled",
        },
        "ecoFriendly": {
            "ecoFriendlyMode": "eco_friendly_mode",
        },
        "sabbath": {
            "sabbathMode": "sabbath_mode",
        },
        "refrigeration": {
            "rapidFreeze": "rapid_freeze",
            "expressMode": "express_mode",
            "freshAirFilter": "fresh_air_filter",
        },
        "waterFilterInfo": {
            "usedTime": "used_time",
            "unit": "water_filter_info_unit",
        },
    }

    _DOOR_LOCATION_MAP = {"MAIN": "main"}
    _TEMPERATURE_LOCATION_MAP = {
        "FRIDGE": "fridge",
        "FREEZER": "freezer",
        "CONVERTIBLE": "convertible",
    }

    def __init__(self, profile: dict[str, Any]):
        _location_properties = {}
        super().__init__(profile)

        for location_property in profile.get("property", {}).get("doorStatus", []):
            location_name = location_property.get("locationName")
            if location_name in self._DOOR_LOCATION_MAP.keys():
                attr_key = self._DOOR_LOCATION_MAP[location_name]
                _sub_profile = RefrigeratorSubProfile(profile, location_name)
                setattr(self, attr_key, _sub_profile)
                _location_properties[attr_key] = _sub_profile.properties

        for location_property in profile.get("property", {}).get("temperature", []):
            location_name = location_property.get("locationName")
            if location_name in self._TEMPERATURE_LOCATION_MAP.keys():
                attr_key = self._TEMPERATURE_LOCATION_MAP[location_name]
                _sub_profile = RefrigeratorSubProfile(profile, location_name)
                setattr(self, attr_key, _sub_profile)
                _location_properties[attr_key] = _sub_profile.properties
        self._location_properties = _location_properties

    def get_location_key(self, location_name: str) -> str | None:
        for key, name in self._DOOR_LOCATION_MAP.items():
            if name == location_name:
                return key
        for key, name in self._TEMPERATURE_LOCATION_MAP.items():
            if name == location_name:
                return key


class RefrigeratorSubDevice(ConnectSubDevice):
    """Refrigerator Device Sub."""

    def __init__(
        self,
        profiles: RefrigeratorSubProfile,
        location_name: str,
        thinq_api: ThinQApi,
        device_id: str,
        device_type: str,
        model_name: str,
        alias: str,
        reportable: bool,
    ):
        super().__init__(
            profiles,
            location_name,
            thinq_api,
            device_id,
            device_type,
            model_name,
            alias,
            reportable,
            is_single_resource=True,
        )

    @property
    def profiles(self) -> RefrigeratorSubProfile:
        return self._profiles

    async def set_target_temperature(self, temperature: float) -> ThinQApiResponse:
        _resource_key = "temperature"
        _target_temperature_key, _unit_key = self.get_property_keys(_resource_key, ["targetTemperature", "unit"])

        _payload = self.profiles.get_range_attribute_payload(_target_temperature_key, temperature)
        _payload[_resource_key] = dict(
            {
                "locationName": self._location_name,
                "unit": self.get_status(_unit_key),
            },
            **(_payload[_resource_key]),
        )
        return await self._do_attribute_command(_payload)


class RefrigeratorDevice(ConnectMainDevice):
    """Refrigerator Property."""

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
        self._sub_devices: dict[str, RefrigeratorSubDevice] = {}
        super().__init__(
            thinq_api=thinq_api,
            device_id=device_id,
            device_type=device_type,
            model_name=model_name,
            alias=alias,
            reportable=reportable,
            profiles=RefrigeratorProfile(profile=profile),
            sub_device_type=RefrigeratorSubDevice,
        )

    @property
    def profiles(self) -> RefrigeratorProfile:
        return self._profiles

    def get_sub_device(self, location_name: str) -> RefrigeratorSubDevice:
        return super().get_sub_device(location_name)

    async def set_rapid_freeze(self, mode: bool) -> ThinQApiResponse:
        return await self.do_attribute_command("rapid_freeze", mode)

    async def set_express_mode(self, mode: bool) -> ThinQApiResponse:
        return await self.do_attribute_command("express_mode", mode)

    async def set_fresh_air_filter(self, mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("fresh_air_filter", mode)
