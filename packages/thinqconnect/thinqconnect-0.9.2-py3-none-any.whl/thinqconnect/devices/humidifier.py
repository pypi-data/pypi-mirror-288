from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .connect_device import ConnectBaseDevice, ConnectDeviceProfile


class HumidifierProfile(ConnectDeviceProfile):
    _RESOURCE_MAP = {
        "humidifierJobMode": "humidifier_job_mode",
        "operation": "operation",
        "timer": "timer",
        "sleepTimer": "sleep_timer",
        "humidity": "humidity",
        "airFlow": "air_flow",
        "airQualitySensor": "air_quality_sensor",
        "display": "display",
        "moodLamp": "mood_lamp",
    }
    _PROFILE = {
        "humidifierJobMode": {
            "currentJobMode": "current_job_mode",
        },
        "operation": {
            "humidifierOperationMode": "humidifier_operation_mode",
            "autoMode": "auto_mode",
            "sleepMode": "sleep_mode",
            "hygieneDryMode": "hygiene_dry_mode",
        },
        "timer": {
            "absoluteHourToStart": "absolute_hour_to_start",
            "absoluteHourToStop": "absolute_hour_to_stop",
            "absoluteMinuteToStart": "absolute_minute_to_start",
            "absoluteMinuteToStop": "absolute_minute_to_stop",
        },
        "sleepTimer": {
            "relativeHourToStop": "sleep_timer_relative_hour_to_stop",
            "relativeMinuteToStop": "sleep_timer_relative_minute_to_stop",
        },
        "humidity": {
            "targetHumidity": "target_humidity",
            "warmMode": "warm_mode",
        },
        "airFlow": {
            "windStrength": "wind_strength",
        },
        "airQualitySensor": {
            "monitoringEnabled": "monitoring_enabled",
            "totalPollution": "total_pollution",
            "PM1": "pm1",
            "PM2": "pm2",
            "PM10": "pm10",
            "humidity": "humidity",
            "temperature": "temperature",
        },
        "display": {
            "light": "display_light",
        },
        "moodLamp": {
            "moodLampState": "mood_lamp_state",
        },
    }


class HumidifierDevice(ConnectBaseDevice):
    _CUSTOM_SET_PROPERTY_NAME = {
        "absolute_hour_to_start": "absolute_time_to_start",
        "absolute_minute_to_start": "absolute_time_to_start",
        "absolute_hour_to_stop": "absolute_time_to_stop",
        "absolute_minute_to_stop": "absolute_time_to_stop",
        "sleep_timer_relative_hour_to_stop": "sleep_timer_relative_time_to_stop",
        "sleep_timer_relative_minute_to_stop": "sleep_timer_relative_time_to_stop",
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
            profiles=HumidifierProfile(profile=profile),
        )

    @property
    def profiles(self) -> HumidifierProfile:
        return self._profiles

    async def set_current_job_mode(self, job_mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("current_job_mode", job_mode)

    async def set_humidifier_operation_mode(self, operation_mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("humidifier_operation_mode", operation_mode)

    async def set_auto_mode(self, auto_mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("auto_mode", auto_mode)

    async def set_sleep_mode(self, sleep_mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("sleep_mode", sleep_mode)

    async def set_hygiene_dry_mode(self, hygiene_dry_mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("hygiene_dry_mode", hygiene_dry_mode)

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

    async def set_target_humidity(self, target_humidity: int) -> ThinQApiResponse:
        return await self.do_attribute_command("target_humidity", target_humidity)

    async def set_warm_mode(self, warm_mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("warm_mode", warm_mode)

    async def set_wind_strength(self, wind_strength: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("wind_strength", wind_strength)

    async def set_display_light(self, display_light: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("display_light", display_light)

    async def set_mood_lamp_state(self, state: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("mood_lamp_state", state)
