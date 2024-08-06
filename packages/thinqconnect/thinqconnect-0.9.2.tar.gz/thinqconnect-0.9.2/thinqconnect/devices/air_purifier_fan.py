from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .connect_device import ConnectBaseDevice, ConnectDeviceProfile


class AirPurifierFanProfile(ConnectDeviceProfile):
    _RESOURCE_MAP = {
        "airFanJobMode": "air_fan_job_mode",
        "operation": "operation",
        "timer": "timer",
        "sleepTimer": "sleep_timer",
        "airFlow": "air_flow",
        "airQualitySensor": "air_quality_sensor",
        "display": "display",
        "misc": "misc",
    }
    _PROFILE = {
        "airFanJobMode": {"currentJobMode": "current_job_mode"},
        "operation": {"airFanOperationMode": "air_fan_operation_mode"},
        "timer": {
            "absoluteHourToStart": "absolute_hour_to_start",
            "absoluteMinuteToStart": "absolute_minute_to_start",
            "absoluteHourToStop": "absolute_hour_to_stop",
            "absoluteMinuteToStop": "absolute_minute_to_stop",
        },
        "sleepTimer": {
            "relativeHourToStop": "sleep_timer_relative_hour_to_stop",
            "relativeMinuteToStop": "sleep_timer_relative_minute_to_stop",
        },
        "airFlow": {
            "warmMode": "warm_mode",
            "windTemperature": "wind_temperature",
            "windStrength": "wind_strength",
            "windAngle": "wind_angle",
        },
        "airQualitySensor": {
            "monitoringEnabled": "monitoring_enabled",
            "PM1": "pm1",
            "PM2": "pm2",
            "PM10": "pm10",
            "humidity": "humidity",
            "temperature": "temperature",
            "odor": "odor",
            "totalPollution": "total_pollution",
        },
        "display": {"light": "display_light"},
        "misc": {"uvNano": "uv_nano"},
    }


class AirPurifierFanDevice(ConnectBaseDevice):
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
            profiles=AirPurifierFanProfile(profile=profile),
        )

    @property
    def profiles(self) -> AirPurifierFanProfile:
        return self._profiles

    async def set_current_job_mode(self, job_mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("current_job_mode", job_mode)

    async def set_air_fan_operation_mode(self, operation_mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("air_fan_operation_mode", operation_mode)

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

    async def set_sleep_timer_relative_time_to_stop(self, hour: int, minute: int = 0) -> ThinQApiResponse:
        return await self.do_multi_attribute_command(
            {
                "sleep_timer_relative_hour_to_stop": hour,
                **({"sleep_timer_relative_minute_to_stop": minute} if minute != 0 else {}),
            }
        )

    async def set_warm_mode(self, warm_mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("warm_mode", warm_mode)

    async def set_wind_temperature(self, wind_temperature: int) -> ThinQApiResponse:
        return await self.do_attribute_command("wind_temperature", wind_temperature)

    async def set_wind_strength(self, wind_strength: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("wind_strength", wind_strength)

    async def set_wind_angle(self, wind_angle: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("wind_angle", wind_angle)

    async def set_display_light(self, display_light: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("display_light", display_light)

    async def set_uv_nano(self, uv_nano: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("uv_nano", uv_nano)
