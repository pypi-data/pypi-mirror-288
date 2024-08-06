from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .connect_device import ConnectBaseDevice, ConnectDeviceProfile


class DryerProfile(ConnectDeviceProfile):
    """Dryer Profile."""

    _RESOURCE_MAP = {
        "runState": "run_state",
        "operation": "operation",
        "remoteControlEnable": "remote_control_enable",
        "timer": "timer",
    }

    _PROFILE = {
        "runState": {"currentState": "current_state"},
        "operation": {
            "dryerOperationMode": "dryer_operation_mode",
        },
        "remoteControlEnable": {"remoteControlEnabled": "remote_control_enabled"},
        "timer": {
            "remainHour": "remain_hour",
            "remainMinute": "remain_minute",
            "totalHour": "total_hour",
            "totalMinute": "total_minute",
            "relativeHourToStop": "relative_hour_to_stop",
            "relativeMinuteToStop": "relative_minute_to_stop",
            "relativeHourToStart": "relative_hour_to_start",
            "relativeMinuteToStart": "relative_minute_to_start",
        },
    }


class DryerDevice(ConnectBaseDevice):
    """Dryer Property."""

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
            profiles=DryerProfile(profile=profile),
        )

    @property
    def profiles(self) -> DryerProfile:
        return self._profiles

    async def set_dryer_operation_mode(self, mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("dryer_operation_mode", mode)

    async def set_relative_hour_to_start(self, hour: int) -> ThinQApiResponse:
        return await self.do_attribute_command("relative_hour_to_start", hour)

    async def set_relative_hour_to_stop(self, hour: int) -> ThinQApiResponse:
        return await self.do_range_attribute_command("relative_hour_to_stop", hour)
