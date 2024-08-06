from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .connect_device import ConnectBaseDevice, ConnectDeviceProfile


class StylerProfile(ConnectDeviceProfile):
    """Styler Profile."""

    _RESOURCE_MAP = {
        "runState": "run_state",
        "operation": "operation",
        "remoteControlEnable": "remote_control_enable",
        "timer": "timer",
    }

    _PROFILE = {
        "runState": {"currentState": "current_state"},
        "operation": {"stylerOperationMode": "styler_operation_mode"},
        "remoteControlEnable": {"remoteControlEnabled": "remote_control_enabled"},
        "timer": {
            "relativeHourToStop": "relative_hour_to_stop",
            "relativeMinuteToStop": "relative_minute_to_stop",
            "remainHour": "remain_hour",
            "remainMinute": "remain_minute",
            "totalHour": "total_hour",
            "totalMinute": "total_minute",
        },
    }


class StylerDevice(ConnectBaseDevice):
    """Styler Property."""

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
            profiles=StylerProfile(profile=profile),
        )

    @property
    def profiles(self) -> StylerProfile:
        return self._profiles

    async def set_styler_operation_mode(self, mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("styler_operation_mode", mode)

    async def set_relative_hour_to_stop(self, hour: int) -> ThinQApiResponse:
        return await self.do_range_attribute_command("relative_hour_to_stop", hour)
