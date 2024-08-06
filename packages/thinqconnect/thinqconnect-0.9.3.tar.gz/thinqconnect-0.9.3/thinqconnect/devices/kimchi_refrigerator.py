from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi
from .connect_device import READABLE_VALUES, WRITABLE_VALUES, ConnectDeviceProfile, ConnectMainDevice, ConnectSubDevice


class KimchiRefrigeratorSubProfile(ConnectDeviceProfile):
    """KimchiRefrigerator Profile."""

    _PROFILE = {
        "temperature": {
            "targetTemperature": "target_temperature",
        },
    }
    _CUSTOM_RESOURCES = ["temperature"]
    _RESOURCE_MAP = {
        "temperature": "temperature",
    }

    def __init__(self, profile: dict[str, Any], location_name: str):
        self._location_name = location_name
        super().__init__(profile)

    def _generate_custom_resource_properties(
        self, resource_key: str, resource_property: dict | list, props: dict[str, str]
    ) -> tuple[list[str], list[str]]:
        # pylint: disable=unused-argument
        readable_props = []
        writable_props = []
        for _temperature in resource_property:
            if _temperature["locationName"] == self._location_name:
                attr_name = self._PROFILE["temperature"]["targetTemperature"]
                prop = self._get_properties(_temperature, "targetTemperature")
                self._set_prop_attr(attr_name, prop)
                if prop[READABLE_VALUES]:
                    readable_props.append(attr_name)
                if prop[WRITABLE_VALUES]:
                    writable_props.append(attr_name)

        return readable_props, writable_props


class KimchiRefrigeratorProfile(ConnectDeviceProfile):
    """KimchiRefrigerator Profile."""

    _RESOURCE_MAP = {"refrigeration": "refrigeration"}
    _PROFILE = {
        "refrigeration": {
            "oneTouchFilter": "one_touch_filter",
            "freshAirFilter": "fresh_air_filter",
        },
    }

    _LOCATION_MAP = {
        "TOP": "top",
        "MIDDLE": "middle",
        "BOTTOM": "bottom",
        "LEFT": "left",
        "RIGHT": "right",
        "SINGLE": "single",
    }

    def __init__(self, profile: dict[str, Any]):
        _location_properties = {}
        super().__init__(profile)

        for temperature_property in profile.get("property", {}).get("temperature", []):
            location_name = temperature_property.get("locationName")
            if location_name in self._LOCATION_MAP.keys():
                attr_key = self._LOCATION_MAP[location_name]
                _sub_profile = KimchiRefrigeratorSubProfile(profile, location_name)
                setattr(self, attr_key, _sub_profile)
                _location_properties[attr_key] = _sub_profile.properties
        self._location_properties = _location_properties


class KimchiRefrigeratorSubDevice(ConnectSubDevice):
    """KimchiRefrigerator Device Sub."""

    def __init__(
        self,
        profiles: KimchiRefrigeratorSubProfile,
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
    def profiles(self) -> KimchiRefrigeratorSubProfile:
        return self._profiles


class KimchiRefrigeratorDevice(ConnectMainDevice):
    """KimchiRefrigerator Property."""

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
        self._sub_devices: dict[str, KimchiRefrigeratorSubDevice] = {}
        super().__init__(
            thinq_api=thinq_api,
            device_id=device_id,
            device_type=device_type,
            model_name=model_name,
            alias=alias,
            reportable=reportable,
            profiles=KimchiRefrigeratorProfile(profile=profile),
            sub_device_type=KimchiRefrigeratorSubDevice,
        )

    @property
    def profiles(self) -> KimchiRefrigeratorProfile:
        return self._profiles

    def get_sub_device(self, location_name: str) -> KimchiRefrigeratorSubDevice:
        return super().get_sub_device(location_name)
