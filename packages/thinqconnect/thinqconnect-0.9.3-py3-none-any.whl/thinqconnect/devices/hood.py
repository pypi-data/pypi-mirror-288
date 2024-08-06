from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi, ThinQApiResponse
from .connect_device import ConnectBaseDevice, ConnectDeviceProfile


class HoodProfile(ConnectDeviceProfile):
    """Hood Profile."""

    _RESOURCE_MAP = {
        "ventilation": "ventilation",
        "lamp": "lamp",
        "operation": "operation",
        "timer": "timer",
    }

    _PROFILE = {
        "ventilation": {
            "fanSpeed": "fan_speed",
        },
        "lamp": {
            "lampBrightness": "lamp_brightness",
        },
        "operation": {
            "hoodOperationMode": "hood_operation_mode",
        },
        "timer": {
            "remainMinute": "remain_minute",
            "remainSecond": "remain_second",
        },
    }


class HoodDevice(ConnectBaseDevice):
    """Oven Property."""

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
            profiles=HoodProfile(profile=profile),
        )

    @property
    def profiles(self) -> HoodProfile:
        return self._profiles

    @property
    def remain_time(self) -> dict:
        return {"minute": self.remain_minute, "second": self.remain_second}

    async def set_fan_speed_lamp_brightness(self, fan_speed: int, lamp_brightness: int) -> ThinQApiResponse:
        return await self.do_multi_range_attribute_command(
            {
                "fan_speed": fan_speed,
                "lamp_brightness": lamp_brightness,
            }
        )

    async def set_fan_speed(self, fan_speed: int) -> ThinQApiResponse:
        return await self.do_multi_range_attribute_command(
            {"fan_speed": fan_speed, "lamp_brightness": self.lamp_brightness}
        )

    async def set_lamp_brightness(self, lamp_brightness: int) -> ThinQApiResponse:
        return await self.do_multi_range_attribute_command(
            {
                "fan_speed": self.fan_speed,
                "lamp_brightness": lamp_brightness,
            }
        )
