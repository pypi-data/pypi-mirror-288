from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .connect_device import ConnectBaseDevice, ConnectDeviceProfile


class MicrowaveOvenProfile(ConnectDeviceProfile):
    _RESOURCE_MAP = {
        "runState": "run_state",
        "timer": "timer",
        "ventilation": "ventilation",
        "lamp": "lamp",
    }

    _PROFILE = {
        "runState": {"currentState": "current_state"},
        "timer": {
            "remainMinute": "remain_minute",
            "remainSecond": "remain_second",
        },
        "ventilation": {"fanSpeed": "fan_speed"},
        "lamp": {"lampBrightness": "lamp_brightness"},
    }


class MicrowaveOvenDevice(ConnectBaseDevice):
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
            profiles=MicrowaveOvenProfile(profile=profile),
        )

    @property
    def profiles(self) -> MicrowaveOvenProfile:
        return self._profiles

    async def set_fan_speed_lamp_brightness(self, fan_speed: int, lamp_brightness: int) -> ThinQApiResponse:
        return await self.do_multi_range_attribute_command(
            {
                "fan_speed": fan_speed,
                "lamp_brightness": lamp_brightness,
            }
        )

    async def set_fan_speed(self, speed: int) -> ThinQApiResponse:
        return await self.do_multi_range_attribute_command(
            {
                "lamp_brightness": self.get_status("lamp_brightness"),
                "fan_speed": speed,
            }
        )

    async def set_lamp_brightness(self, brightness: int) -> ThinQApiResponse:
        return await self.do_multi_range_attribute_command(
            {
                "lamp_brightness": brightness,
                "fan_speed": self.get_status("fan_speed"),
            }
        )
