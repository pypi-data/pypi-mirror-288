from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .connect_device import ConnectBaseDevice, ConnectDeviceProfile


class DishWasherProfile(ConnectDeviceProfile):
    """DishWasher Profile."""

    _RESOURCE_MAP = {
        "runState": "run_state",
        "dishWashingStatus": "dish_washing_status",
        "preference": "preference",
        "doorStatus": "door_status",
        "operation": "operation",
        "remoteControlEnable": "remote_control_enable",
        "timer": "timer",
        "dishWashingCourse": "dish_washing_course",
    }

    _PROFILE = {
        "runState": {"currentState": "current_state"},
        "dishWashingStatus": {"rinseRefill": "rinse_refill"},
        "preference": {
            "rinseLevel": "rinse_level",
            "softeningLevel": "softening_level",
            "mCReminder": "machine_clean_reminder",
            "signalLevel": "signal_level",
            "cleanLReminder": "clean_light_reminder",
        },
        "doorStatus": {"doorState": "door_state"},
        "operation": {"dishWasherOperationMode": "dish_washer_operation_mode"},
        "remoteControlEnable": {"remoteControlEnabled": "remote_control_enabled"},
        "timer": {
            "relativeHourToStart": "relative_hour_to_start",
            "relativeMinuteToStart": "relative_minute_to_start",
            "remainHour": "remain_hour",
            "remainMinute": "remain_minute",
            "totalHour": "total_hour",
            "totalMinute": "total_minute",
        },
        "dishWashingCourse": {"currentDishWashingCourse": "current_dish_washing_course"},
    }


class DishWasherDevice(ConnectBaseDevice):
    """DishWasher Property."""

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
            profiles=DishWasherProfile(profile=profile),
        )

    @property
    def profiles(self) -> DishWasherProfile:
        return self._profiles

    async def set_dish_washer_operation_mode(self, mode: str) -> ThinQApiResponse:
        return await self.do_enum_attribute_command("dish_washer_operation_mode", mode)

    async def set_relative_hour_to_start(self, hour: int) -> ThinQApiResponse:
        return await self.do_attribute_command("relative_hour_to_start", hour)
