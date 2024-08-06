from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .connect_device import ConnectBaseDevice, ConnectDeviceProfile


class SystemBoilerProfile(ConnectDeviceProfile):
    """SystemBoiler Profile."""

    _RESOURCE_MAP = {
        "boilerJobMode": "boiler_job_mode",
        "operation": "operation",
        "temperature": "temperature",
    }
    _PROFILE = {
        "boilerJobMode": {"currentJobMode": "current_job_mode"},
        "operation": {
            "boilerOperationMode": "boiler_operation_mode",
            "hotWaterMode": "hot_water_mode",
        },
        "temperature": {
            "currentTemperature": "current_temperature",
            "targetTemperature": "target_temperature",
            "heatTargetTemperature": "heat_target_temperature",
            "coolTargetTemperature": "cool_target_temperature",
            "heatMaxTemperature": "heat_max_temperature",
            "heatMinTemperature": "heat_min_temperature",
            "coolMaxTemperature": "cool_max_temperature",
            "coolMinTemperature": "cool_min_temperature",
            "unit": "temperature_unit",
        },
    }


class SystemBoilerDevice(ConnectBaseDevice):
    """SystemBoiler Property."""

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
            profiles=SystemBoilerProfile(profile=profile),
        )

    @property
    def profiles(self) -> SystemBoilerProfile:
        return self._profiles

    async def set_boiler_operation_mode(self, mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("boiler_operation_mode", mode)

    async def set_current_job_mode(self, mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("current_job_mode", mode)

    async def set_hot_water_mode(self, mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("hot_water_mode", mode)

    async def set_heat_target_temperature(self, temperature: int) -> ThinQApiResponse:
        return await self.do_attribute_command("heat_target_temperature", temperature)

    async def set_cool_target_temperature(self, temperature: int) -> ThinQApiResponse:
        return await self.do_attribute_command("cool_target_temperature", temperature)
