from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi
from .connect_device import ConnectDeviceProfile, ConnectMainDevice, ConnectSubDevice


class PlantCultivatorProfile(ConnectDeviceProfile):
    """PlantCultivator Profile."""

    _LOCATION_MAP = {
        "UPPER": "upper",
        "LOWER": "lower",
    }

    def __init__(self, profile: dict[str, Any]):
        super().__init__(profile, use_sub_profile_only=True)
        _location_properties = {}
        for profile_property in profile.get("property", []):
            location_name = profile_property.get("location", {}).get("locationName")
            if location_name in self._LOCATION_MAP.keys():
                attr_key = self._LOCATION_MAP[location_name]
                _sub_profile = PlantCultivatorSubProfile(profile, location_name)
                setattr(self, attr_key, _sub_profile)
                _location_properties[attr_key] = _sub_profile.properties
        self._location_properties = _location_properties
        self._PROFILE = PlantCultivatorSubProfile._PROFILE


class PlantCultivatorSubProfile(ConnectDeviceProfile):
    """PlantCultivator Profile."""

    _RESOURCE_MAP = {
        "runState": "run_state",
        "light": "light",
        "temperature": "temperature",
    }

    _PROFILE = {
        "runState": {
            "currentState": "current_state",
            "growthMode": "growth_mode",
            "windVolume": "wind_volume",
        },
        "light": {
            "brightness": "brightness",
            "duration": "duration",
            "startHour": "start_hour",
            "startMinute": "start_minute",
            "endHour": "end_hour",
            "endMinute": "end_minute",
        },
        "temperature": {
            "dayTargetTemperature": "day_target_temperature",
            "nightTargetTemperature": "night_target_temperature",
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


class PlantCultivatorSubDevice(ConnectSubDevice):
    def __init__(
        self,
        profiles: PlantCultivatorSubProfile,
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
    def profiles(self) -> PlantCultivatorSubProfile:
        return self._profiles


class PlantCultivatorDevice(ConnectMainDevice):
    """PlantCultivator Property."""

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
        self._sub_devices: dict[str, PlantCultivatorSubDevice] = {}
        super().__init__(
            thinq_api=thinq_api,
            device_id=device_id,
            device_type=device_type,
            model_name=model_name,
            alias=alias,
            reportable=reportable,
            profiles=PlantCultivatorProfile(profile=profile),
            sub_device_type=PlantCultivatorSubDevice,
        )

    @property
    def profiles(self) -> PlantCultivatorProfile:
        return self._profiles

    def get_sub_device(self, location_name: str) -> PlantCultivatorSubDevice:
        return super().get_sub_device(location_name)
