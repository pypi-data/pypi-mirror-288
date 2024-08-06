from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Callable

import pytest

from thinqconnect.const import DeviceType
from thinqconnect.devices.connect_device import ConnectBaseDevice
from thinqconnect.thinq_api import ThinQApi

logger = logging.getLogger("test")


def pytest_generate_tests(metafunc):
    if "model_name" in metafunc.fixturenames:
        device_type = metafunc.cls.get_device_type()
        model_list = get_model_list(device_type)
        metafunc.parametrize("model_name", model_list)


def get_model_list(device_type: str) -> list[str]:
    base_path = Path.cwd() / "tests" / "devices" / device_type.split("DEVICE_")[1].lower()
    return [d.name for d in base_path.iterdir() if d.is_dir()]


@pytest.fixture
def generate_device() -> Callable[[type[ConnectBaseDevice], ThinQApi, dict, str, str, str | None], ConnectBaseDevice]:
    def _device(
        device_class: type[ConnectBaseDevice],
        thinq_api: ThinQApi,
        profile: dict,
        device_type: str,
        model_name: str,
        reportable: bool = False,
        group_id: str | None = None,
    ) -> ConnectBaseDevice:
        if device_type in [
            DeviceType.WASHCOMBO_MAIN,
            DeviceType.WASHCOMBO_MINI,
            DeviceType.WASHTOWER_DRYER,
            DeviceType.WASHTOWER_WASHER,
        ]:
            return device_class(
                thinq_api=thinq_api,
                device_id=profile["deviceId"],
                device_type=device_type,
                model_name=model_name,
                alias=f"TEST_{device_type}",
                reportable=reportable,
                profile=profile["response"],
                group_id=group_id,
            )
        else:
            return device_class(
                thinq_api=thinq_api,
                device_id=profile["deviceId"],
                device_type=device_type,
                model_name=model_name,
                alias=f"TEST_{device_type}",
                reportable=reportable,
                profile=profile["response"],
            )

    return _device


@pytest.fixture
def json_object() -> Callable[[str], dict]:
    def _json_object(file_path: str):
        return read_file(file_path)

    return _json_object


def read_file(file_path: str) -> dict:
    default_dict = {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            sample_set = f.read()
            return json.loads(sample_set)
    except Exception as e:
        logger.error(f"read file error: {e}")
        return default_dict


@pytest.fixture
def test_device_profile() -> Callable[[str, ConnectBaseDevice], dict]:
    def _device_profile(device_name: str, device: ConnectBaseDevice) -> dict:
        profile_attr: dict[str, dict | list | None] = {
            "properties": device.profiles.properties,
            "writable_properties": device.profiles.writable_properties,
            "location_properties": device.profiles.location_properties,
            "notification": device.profiles.notification,
            "errors": device.profiles.errors,
        }
        for key, value in profile_attr.items():
            logger.info(f"test {device_name}.profiles.{key}: {value}")

        test_result = dict.copy(profile_attr)
        for properties in profile_attr["properties"].values():
            for prop in properties:
                test_result[prop] = device.profiles.get_property(prop)
                logger.info(f"test {device_name}.profiles.{prop}: {test_result[prop]}")

        for location, resources in profile_attr["location_properties"].items():
            location_profiles = device.profiles.get_sub_profile(location)
            sub_profile_attr: dict[str, dict | list | None] = {
                "writable_properties": location_profiles.writable_properties,
                **(
                    {"notification": location_profiles.notification, "errors": location_profiles.errors}
                    if location_profiles.notification or location_profiles.errors
                    else {}
                ),
            }
            for key, value in sub_profile_attr.items():
                logger.info(f"test {device_name}.profiles.{location}.{key}: {value}")

            test_result[location] = dict.copy(sub_profile_attr)
            for properties in resources.values():
                for prop in properties:
                    test_result[location][prop] = location_profiles.get_property(prop)
                    logger.info(f"test {device_name}.profiles.{location}.{prop}: {test_result[location][prop]}")

        return test_result

    return _device_profile


@pytest.fixture
def test_device_status() -> Callable[[str, ConnectBaseDevice, dict, bool], dict]:
    def _device_status(device_name: str, device: ConnectBaseDevice, status: dict, is_update: bool = False) -> dict:
        device_properties = device.profiles.properties
        location_properties = device.profiles.location_properties
        if is_update:
            device.update_status(status=status["response"])
        else:
            device.set_status(status=status["response"])

        test_result = {}
        if device.profiles.errors:
            test_result["error"] = device.get_status("error")
            logger.info(f"test {device_name}.error: {test_result['error']}")

        for properties in device_properties.values():
            for prop in properties:
                test_result[prop] = device.get_status(prop)
                logger.info(f"test {device_name}.{prop}: {test_result[prop]}")

        for location, resources in location_properties.items():
            sub_device = device.get_sub_device(location)
            test_result[location] = {}
            if device.profiles.get_sub_profile(location).errors:
                test_result[location]["error"] = sub_device.get_status("error")
                logger.info(f"test {device_name}.{location}.error: {test_result[location]['error']}")

            for properties in resources.values():
                for prop in properties:
                    test_result[location][prop] = sub_device.get_status(prop)
                    logger.info(f"test {device_name}.{location}.{prop}: {test_result[location][prop]}")
        return test_result

    return _device_status


@pytest.fixture
def check_device_control() -> Callable[[str, ConnectBaseDevice], None]:
    def _check_result(fn_name: str | None, prop_name: str) -> str:
        if fn_name == f"set_{prop_name}":
            return "Exist"
        elif fn_name:
            return f"Exist with custom name '{fn_name}'"
        return "Not Exist"

    def _check_control(device_name: str, device: ConnectBaseDevice):
        location_properties = device.profiles.location_properties
        writable_props = device.profiles.writable_properties
        logger.info(f"test {device_name}.profiles.writable_properties: {device.profiles.writable_properties}")
        for prop in writable_props:
            logger.info(f"check {device_name}.set_{prop}: {_check_result(device.get_property_set_fn(prop), prop)}")

        for location in location_properties.keys():
            sub_device = device.get_sub_device(location)
            writable_props = sub_device.profiles.writable_properties
            logger.info(
                f"test {device_name}.profiles.{location}.writable_properties: {sub_device.profiles.writable_properties}"
            )
            for prop in writable_props:
                logger.info(
                    f"check {device_name}.{location}.set_{prop}: {_check_result(sub_device.get_property_set_fn(prop), prop)}"
                )

    return _check_control
