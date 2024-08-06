from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .connect_device import ConnectBaseDevice, ConnectDeviceProfile


class WaterHeaterProfile(ConnectDeviceProfile):
    """WaterHeater Profile."""

    _RESOURCE_MAP = {
        "waterHeaterJobMode": "water_heater_job_mode",
        "operation": "operation",
        "temperature": "temperature",
    }

    _PROFILE = {
        "waterHeaterJobMode": {"currentJobMode": "current_job_mode"},
        "operation": {"waterHeaterOperationMode": "water_heater_operation_mode"},
        "temperature": {
            "currentTemperature": "current_temperature",
            "targetTemperature": "target_temperature",
        },
    }


class WaterHeaterDevice(ConnectBaseDevice):
    """WaterHeater Property."""

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
            profiles=WaterHeaterProfile(profile=profile),
        )

    @property
    def profiles(self) -> WaterHeaterProfile:
        return self._profiles

    async def set_current_job_mode(self, mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("current_job_mode", mode)

    async def set_target_temperature(self, temperature: int) -> ThinQApiResponse:
        return await self.do_attribute_command("target_temperature", temperature)
