from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi
from .connect_device import ConnectBaseDevice, ConnectDeviceProfile


class WaterPurifierProfile(ConnectDeviceProfile):
    """WaterPurifier Profile."""

    _RESOURCE_MAP = {"runState": "run_state", "waterInfo": "water_info"}

    _PROFILE = {
        "runState": {"cockState": "cock_state", "sterilizingState": "sterilizing_state"},
        "waterInfo": {"waterType": "water_type"},
    }


class WaterPurifierDevice(ConnectBaseDevice):
    """WaterPurifier Property."""

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
            profiles=WaterPurifierProfile(profile=profile),
        )

    @property
    def profiles(self) -> WaterPurifierProfile:
        return self._profiles
