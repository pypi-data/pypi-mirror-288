from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .connect_device import ConnectBaseDevice, ConnectDeviceProfile


class DehumidifierProfile(ConnectDeviceProfile):
    _RESOURCE_MAP = {
        "operation": "operation",
        "dehumidifierJobMode": "dehumidifier_job_mode",
        "humidity": "humidity",
        "airFlow": "air_flow",
    }
    _PROFILE = {
        "operation": {"dehumidifierOperationMode": "dehumidifier_operation_mode"},
        "dehumidifierJobMode": {"currentJobMode": "current_job_mode"},
        "humidity": {"currentHumidity": "current_humidity"},
        "airFlow": {"windStrength": "wind_strength"},
    }


class DehumidifierDevice(ConnectBaseDevice):
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
            profiles=DehumidifierProfile(profile=profile),
        )

    @property
    def profiles(self) -> DehumidifierProfile:
        return self._profiles

    async def set_dehumidifier_operation_mode(self, mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("dehumidifier_operation_mode", mode)

    async def set_wind_strength(self, wind_strength: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("wind_strength", wind_strength)
