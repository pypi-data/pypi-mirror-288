from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi
from .connect_device import ConnectBaseDevice, ConnectDeviceProfile


class StickCleanerProfile(ConnectDeviceProfile):
    """StickCleaner Profile."""

    _RESOURCE_MAP = {
        "runState": "run_state",
        "stickCleanerJobMode": "stick_cleaner_job_mode",
        "battery": "battery",
    }

    _PROFILE = {
        "runState": {"currentState": "current_state"},
        "stickCleanerJobMode": {
            "currentJobMode": "current_job_mode",
        },
        "battery": {"level": "battery_level", "percent": "battery_percent"},
    }


class StickCleanerDevice(ConnectBaseDevice):
    """StickCleaner Property."""

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
            profiles=StickCleanerProfile(profile=profile),
        )

    @property
    def profiles(self) -> StickCleanerProfile:
        return self._profiles
