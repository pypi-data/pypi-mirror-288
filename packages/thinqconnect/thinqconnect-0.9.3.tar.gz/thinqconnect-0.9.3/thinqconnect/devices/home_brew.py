from __future__ import annotations

from typing import Any

from ..thinq_api import ThinQApi
from .connect_device import ConnectBaseDevice, ConnectDeviceProfile


class HomeBrewProfile(ConnectDeviceProfile):
    """HomeBrew Profile."""

    _RESOURCE_MAP = {"runState": "run_state", "recipe": "recipe", "timer": "timer"}

    _PROFILE = {
        "runState": {"currentState": "current_state"},
        "recipe": {
            "beerRemain": "beer_remain",
            "flavorInfo": "flavor_info",
            "hopOilInfo": "hop_oil_info",
            "wortInfo": "wort_info",
            "yeastInfo": "yeast_info",
            "recipeName": "recipe_name",
        },
        "timer": {
            "elapsedDayState": "elapsed_day_state",
            "elapsedDayTotal": "elapsed_day_total",
        },
    }


class HomeBrewDevice(ConnectBaseDevice):
    """HomeBrew Property."""

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
            profiles=HomeBrewProfile(profile=profile),
        )

    @property
    def profiles(self) -> HomeBrewProfile:
        return self._profiles
