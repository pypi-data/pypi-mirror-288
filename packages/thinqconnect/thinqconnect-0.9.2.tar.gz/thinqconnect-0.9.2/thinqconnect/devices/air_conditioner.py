from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .connect_device import ConnectBaseDevice, ConnectDeviceProfile


class AirConditionerProfile(ConnectDeviceProfile):
    """Air Conditioner Profile."""

    _RESOURCE_MAP = {
        "airConJobMode": "air_con_job_mode",
        "operation": "operation",
        "temperature": "temperature",
        "twoSetTemperature": "two_set_temperature",
        "timer": "timer",
        "sleepTimer": "sleep_timer",
        "powerSave": "power_save",
        "airFlow": "air_flow",
        "airQualitySensor": "air_quality_sensor",
        "filterInfo": "filter_info",
    }

    _PROFILE = {
        "airConJobMode": {
            "currentJobMode": "current_job_mode",
        },
        "operation": {
            "airConOperationMode": "air_con_operation_mode",
            "airCleanOperationMode": "air_clean_operation_mode",
        },
        "temperature": {
            "currentTemperature": "current_temperature",
            "targetTemperature": "target_temperature",
            "heatTargetTemperature": "heat_target_temperature",
            "coolTargetTemperature": "cool_target_temperature",
            "unit": "temperature_unit",
        },
        "twoSetTemperature": {
            "currentTemperature": "two_set_current_temperature",
            "heatTargetTemperature": "two_set_heat_target_temperature",
            "coolTargetTemperature": "two_set_cool_target_temperature",
            "unit": "two_set_temperature_unit",
        },
        "timer": {
            "relativeHourToStart": "relative_hour_to_start",
            "relativeMinuteToStart": "relative_minute_to_start",
            "relativeHourToStop": "relative_hour_to_stop",
            "relativeMinuteToStop": "relative_minute_to_stop",
            "absoluteHourToStart": "absolute_hour_to_start",
            "absoluteMinuteToStart": "absolute_minute_to_start",
            "absoluteHourToStop": "absolute_hour_to_stop",
            "absoluteMinuteToStop": "absolute_minute_to_stop",
        },
        "sleepTimer": {
            "relativeHourToStop": "sleep_timer_relative_hour_to_stop",
            "relativeMinuteToStop": "sleep_timer_relative_minute_to_stop",
        },
        "powerSave": {
            "powerSaveEnabled": "power_save_enabled",
        },
        "airFlow": {
            "windStrength": "wind_strength",
            "windStep": "wind_step",
        },
        "airQualitySensor": {
            "PM1": "pm1",
            "PM2": "pm2",
            "PM10": "pm10",
            "odor": "odor",
            "humidity": "humidity",
            "totalPollution": "total_pollution",
            "monitoringEnabled": "monitoring_enabled",
        },
        "filterInfo": {
            "usedTime": "used_time",
            "filterLifetime": "filter_lifetime",
        },
    }


class AirConditionerDevice(ConnectBaseDevice):
    """Air Conditioner Property."""

    _CUSTOM_SET_PROPERTY_NAME = {
        "relative_hour_to_start": "relative_time_to_start",
        "relative_minute_to_start": "relative_time_to_start",
        "relative_hour_to_stop": "relative_time_to_stop",
        "relative_minute_to_stop": "relative_time_to_stop",
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
            profiles=AirConditionerProfile(profile=profile),
        )

    @property
    def profiles(self) -> AirConditionerProfile:
        return self._profiles

    async def set_current_job_mode(self, mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("current_job_mode", mode)

    async def set_air_con_operation_mode(self, operation: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("air_con_operation_mode", operation)

    async def set_air_clean_operation_mode(self, operation: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("air_clean_operation_mode", operation)

    async def set_target_temperature(self, temperature: int) -> ThinQApiResponse:
        return await self.do_range_attribute_command("target_temperature", temperature)

    async def set_heat_target_temperature(self, temperature: int) -> ThinQApiResponse:
        return await self.do_range_attribute_command("heat_target_temperature", temperature)

    async def set_cool_target_temperature(self, temperature: int) -> ThinQApiResponse:
        return await self.do_range_attribute_command("cool_target_temperature", temperature)

    async def set_two_set_heat_target_temperature(self, temperature: int) -> ThinQApiResponse:
        return await self.do_multi_attribute_command(
            {
                "two_set_heat_target_temperature": temperature,
                "two_set_cool_target_temperature": self.get_status("two_set_cool_target_temperature"),
            }
        )

    async def set_two_set_cool_target_temperature(self, temperature: int) -> ThinQApiResponse:
        return await self.do_multi_attribute_command(
            {
                "two_set_heat_target_temperature": self.get_status("two_set_heat_target_temperature"),
                "two_set_cool_target_temperature": temperature,
            }
        )

    async def set_relative_time_to_start(self, hour: int, minute: int) -> ThinQApiResponse:
        return await self.do_multi_attribute_command(
            {
                "relative_hour_to_start": hour,
                "relative_minute_to_start": minute,
            }
        )

    async def set_relative_time_to_stop(self, hour: int, minute: int) -> ThinQApiResponse:
        return await self.do_multi_attribute_command(
            {
                "relative_hour_to_stop": hour,
                **({"relative_minute_to_stop": minute} if minute != 0 else {}),
            }
        )

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

    async def set_sleep_timer_relative_time_to_stop(self, hour: int, minute: int) -> ThinQApiResponse:
        return await self.do_multi_attribute_command(
            {
                "sleep_timer_relative_hour_to_stop": hour,
                "sleep_timer_relative_minute_to_stop": minute,
            }
        )

    async def set_power_save_enabled(self, power_save_enabled: bool) -> ThinQApiResponse:
        return await self.do_attribute_command("power_save_enabled", power_save_enabled)

    async def set_wind_strength(self, wind_strength: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("wind_strength", wind_strength)

    async def set_wind_step(self, wind_step: int) -> ThinQApiResponse:
        return await self.do_range_attribute_command("wind_step", wind_step)

    async def set_monitoring_enabled(self, monitoring_enabled: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("monitoring_enabled", monitoring_enabled)
