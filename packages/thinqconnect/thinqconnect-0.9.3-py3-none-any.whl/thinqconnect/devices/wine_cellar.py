from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .connect_device import READABLE_VALUES, WRITABLE_VALUES, ConnectDeviceProfile, ConnectMainDevice, ConnectSubDevice


class WineCellarSubProfile(ConnectDeviceProfile):
    """WineCellar Profile."""

    _RESOURCE_MAP = {"temperature": "temperature"}
    _PROFILE = {
        "temperature": {
            "targetTemperature": "target_temperature",
            "unit": "temperature_unit",
        },
    }
    _CUSTOM_RESOURCES = ["temperature"]

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


class WineCellarProfile(ConnectDeviceProfile):
    """WineCellar Profile."""

    _RESOURCE_MAP = {"operation": "operation"}
    _PROFILE = {
        "operation": {
            "lightBrightness": "light_brightness",
            "optimalHumidity": "optimal_humidity",
            "sabbathMode": "sabbath_mode",
            "lightStatus": "light_status",
        },
    }
    _CUSTOM_RESOURCES = ["temperature"]

    _LOCATION_MAP = {
        "WINE_UPPER": "upper",
        "WINE_MIDDLE": "middle",
        "WINE_LOWER": "lower",
    }

    def __init__(self, profile: dict[str, Any]):
        _location_properties = {}
        super().__init__(profile)

        for location_property in profile.get("property", {}).get("temperature", []):
            location_name = location_property.get("locationName")
            if location_name in self._LOCATION_MAP.keys():
                attr_key = self._LOCATION_MAP[location_name]
                _sub_profile = WineCellarSubProfile(profile, location_name)
                setattr(self, attr_key, _sub_profile)
                _location_properties[attr_key] = _sub_profile.properties
        self._location_properties = _location_properties


class WineCellarSubDevice(ConnectSubDevice):
    """WineCellar Device Sub."""

    def __init__(
        self,
        profiles: WineCellarSubProfile,
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
    def profiles(self) -> WineCellarSubProfile:
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


class WineCellarDevice(ConnectMainDevice):
    """WineCellar Property."""

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
        self._sub_devices: dict[str, WineCellarSubDevice] = {}
        super().__init__(
            thinq_api=thinq_api,
            device_id=device_id,
            device_type=device_type,
            model_name=model_name,
            alias=alias,
            reportable=reportable,
            profiles=WineCellarProfile(profile=profile),
            sub_device_type=WineCellarSubDevice,
        )

    @property
    def profiles(self) -> WineCellarProfile:
        return self._profiles

    def get_sub_device(self, location_name: str) -> WineCellarSubDevice:
        return super().get_sub_device(location_name)

    async def set_light_brightness(self, brightness_input: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("light_brightness", brightness_input)

    async def set_optimal_humidity(self, humidity_input: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("optimal_humidity", humidity_input)

    async def set_light_status(self, status_input: int) -> ThinQApiResponse:
        return await self.do_range_attribute_command("light_status", status_input)
