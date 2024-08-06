from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .connect_device import ConnectBaseDevice, ConnectDeviceProfile


class CeilingFanProfile(ConnectDeviceProfile):
    """CeilingFan Profile."""

    _RESOURCE_MAP = {"airFlow": "air_flow", "operation": "operation"}

    _PROFILE = {
        "airFlow": {"windStrength": "wind_strength"},
        "operation": {"ceilingfanOperationMode": "ceiling_fan_operation_mode"},
    }


class CeilingFanDevice(ConnectBaseDevice):
    """CeilingFan Property."""

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
            profiles=CeilingFanProfile(profile=profile),
        )

    @property
    def profiles(self) -> CeilingFanProfile:
        return self._profiles

    async def set_wind_strength(self, wind_strength: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("wind_strength", wind_strength)

    async def set_ceiling_fan_operation_mode(self, mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("ceiling_fan_operation_mode", mode)
