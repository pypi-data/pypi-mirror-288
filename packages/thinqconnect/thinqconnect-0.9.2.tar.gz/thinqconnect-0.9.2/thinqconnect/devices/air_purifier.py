from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .connect_device import ConnectBaseDevice, ConnectDeviceProfile


class AirPurifierProfile(ConnectDeviceProfile):
    _RESOURCE_MAP = {
        "airPurifierJobMode": "air_purifier_job_mode",
        "operation": "operation",
        "timer": "timer",
        "airFlow": "air_flow",
        "airQualitySensor": "air_quality_sensor",
    }
    _PROFILE = {
        "airPurifierJobMode": {
            "currentJobMode": "current_job_mode",
            "personalizationMode": "personalization_mode",
        },
        "operation": {"airPurifierOperationMode": "air_purifier_operation_mode"},
        "timer": {
            "absoluteHourToStart": "absolute_hour_to_start",
            "absoluteMinuteToStart": "absolute_minute_to_start",
            "absoluteHourToStop": "absolute_hour_to_stop",
            "absoluteMinuteToStop": "absolute_minute_to_stop",
        },
        "airFlow": {
            "windStrength": "wind_strength",
        },
        "airQualitySensor": {
            "monitoringEnabled": "monitoring_enabled",
            "PM1": "pm1",
            "PM2": "pm2",
            "PM10": "pm10",
            "odor": "odor",
            "humidity": "humidity",
            "totalPollution": "total_pollution",
        },
    }


class AirPurifierDevice(ConnectBaseDevice):
    _CUSTOM_SET_PROPERTY_NAME = {
        "absolute_hour_to_start": "absolute_time_to_start",
        "absolute_minute_to_start": "absolute_time_to_start",
        "absolute_hour_to_stop": "absolute_time_to_stop",
        "absolute_minute_to_stop": "absolute_time_to_stop",
    }

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
            profiles=AirPurifierProfile(profile=profile),
        )

    @property
    def profiles(self) -> AirPurifierProfile:
        return self._profiles

    async def set_current_job_mode(self, job_mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("current_job_mode", job_mode)

    async def set_air_purifier_operation_mode(self, operation_mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("air_purifier_operation_mode", operation_mode)

    async def set_absolute_time_to_start(self, hour: int, minute: int) -> ThinQApiResponse:
        return await self.do_multi_attribute_command(
            {
                "absolute_hour_to_start": hour,
                "absolute_minute_to_start": minute,
            }
        )

    async def set_absolute_time_to_stop(self, hour: int, minute: int) -> ThinQApiResponse:
        return await self.do_multi_attribute_command(
            {
                "absolute_hour_to_stop": hour,
                "absolute_minute_to_stop": minute,
            }
        )

    async def set_wind_strength(self, wind_strength: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("wind_strength", wind_strength)
