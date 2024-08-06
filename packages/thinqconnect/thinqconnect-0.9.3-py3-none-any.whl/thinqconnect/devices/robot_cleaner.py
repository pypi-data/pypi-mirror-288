from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .connect_device import ConnectBaseDevice, ConnectDeviceProfile


class RobotCleanerProfile(ConnectDeviceProfile):
    """RobotCleaner Profile."""

    _RESOURCE_MAP = {
        "runState": "run_state",
        "robotCleanerJobMode": "robot_cleaner_job_mode",
        "operation": "operation",
        "battery": "battery",
        "timer": "timer",
    }

    _PROFILE = {
        "runState": {"currentState": "current_state"},
        "robotCleanerJobMode": {"currentJobMode": "current_job_mode"},
        "operation": {"cleanOperationMode": "clean_operation_mode"},
        "battery": {"level": "battery_level", "percent": "battery_percent"},
        "timer": {
            "absoluteHourToStart": "absolute_hour_to_start",
            "absoluteMinuteToStart": "absolute_minute_to_start",
            "runningHour": "running_hour",
            "runningMinute": "running_minute",
        },
    }


class RobotCleanerDevice(ConnectBaseDevice):
    """RobotCleaner Property."""

    _CUSTOM_SET_PROPERTY_NAME = {
        "absolute_hour_to_start": "absolute_time_to_start",
        "absolute_minute_to_start": "absolute_time_to_start",
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
            profiles=RobotCleanerProfile(profile=profile),
        )

    @property
    def profiles(self) -> RobotCleanerProfile:
        return self._profiles

    async def set_clean_operation_mode(self, mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("clean_operation_mode", mode)

    async def set_absolute_time_to_start(self, hour: int, minute: int) -> ThinQApiResponse:
        return await self.do_multi_attribute_command(
            {
                "absolute_hour_to_start": hour,
                **({"absolute_minute_to_start": minute} if minute != 0 else {}),
            }
        )
