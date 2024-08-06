import abc
import json
import logging
import os
from glob import glob
from typing import Callable

import pytest
from aiohttp import ClientSession
from deepdiff import DeepDiff

from thinqconnect.devices.connect_device import ConnectBaseDevice
from thinqconnect.thinq_api import ThinQApi

logger = logging.getLogger("test")


class DeviceTestBase(abc.ABC):
    @pytest.mark.asyncio
    async def test_device(
        self,
        model_name: str,
        generate_device: Callable[[type[ConnectBaseDevice], ThinQApi, dict, str, str, str | None], ConnectBaseDevice],
        json_object: Callable[[str], dict],
        test_device_profile: Callable[[str, ConnectBaseDevice], dict],
        test_device_status: Callable[[str, ConnectBaseDevice, dict, bool], dict],
        check_device_control: Callable[[str, ConnectBaseDevice], None],
    ):
        async with ClientSession() as session:
            access_token, client_id = self.get_credentials()
            thinq_api = ThinQApi(
                session=session,
                access_token=access_token,
                country_code="KR",
                client_id=client_id,
            )
            device = generate_device(
                self.get_device_class(),
                thinq_api,
                json_object(self.get_profile_file_path(self.get_device_type(), model_name)),
                self.get_device_type(),
                model_name,
            )

            await self.run_device_test(
                device,
                json_object,
                test_device_profile,
                test_device_status,
                check_device_control,
            )

    @classmethod
    def get_credentials(cls) -> tuple[str, str]:
        access_token = "ab3f3fa8443d91d48a2e331c6489ae0c1133acd441e539035ac1"
        client_id = "test_client_id"
        return (access_token, client_id)

    @classmethod
    def get_device_type_path(cls, device_type: str) -> str:
        short_device_type = cls.get_short_device_type(device_type)
        return f"tests/devices/{short_device_type}/"

    @classmethod
    def get_profile_file_path(cls, device_type: str, model_name: str) -> str:
        return f"{cls.get_device_type_path(device_type)}{model_name}/profile.json"

    @classmethod
    def get_result_file_path(cls, device_type: str, model_name: str) -> str:
        return f"{cls.get_device_type_path(device_type)}result_{model_name}.json"

    @classmethod
    def get_short_device_type(cls, device_type: str) -> str:
        return device_type.split("DEVICE_")[1].lower()

    @classmethod
    def write_test_result(cls, device_type: str, model_name: str, test_result: dict) -> str:
        try:
            file_path = cls.get_result_file_path(device_type, model_name)
            if file_exist := os.path.exists(file_path):
                with open(file_path) as file:
                    if file:
                        prev_result = json.load(file)
                        if not DeepDiff(prev_result, test_result, ignore_order=True):
                            logger.info("Test Result is not Changed.")
                            return

            with open(file_path, "w") as file:
                json.dump(test_result, file, indent=4)

        except Exception as e:
            logger.info(f"An error occurred: {e}")

        if not file_exist:
            logger.info(f"Test Result is Created to {file_path}")
        else:
            logger.info(f"Test Result is Updated to {file_path}")
            assert False

    @classmethod
    async def run_device_test(
        cls,
        device: ConnectBaseDevice,
        json_object: Callable[[str], dict],
        test_device_profile: Callable[[str, ConnectBaseDevice], dict],
        test_device_status: Callable[[str, ConnectBaseDevice, dict, bool], dict],
        check_device_control: Callable[[str, ConnectBaseDevice], None],
    ):
        device_type = device.device_type
        short_device_type = cls.get_short_device_type(device_type)
        model_name = device.model_name
        test_result = {"profile": None, "status": {}, "event": {}}

        logger.info(f"{device_type} Test with model : {model_name}")

        test_result["profile"] = test_device_profile(device_type, device)

        status_files = glob(f"tests/devices/{short_device_type}/{model_name}/status/*.json")
        for status_file in status_files:
            status = json_object(status_file)
            test_result["status"][status_file.split("/")[-1]] = test_device_status(device_type, device, status)

        event_files = glob(f"tests/devices/{short_device_type}/{model_name}/event/*.json")

        for event_file in sorted(event_files):
            print(event_file.split("/")[-1])
            event = json_object(event_file)
            test_result["event"][event_file.split("/")[-1]] = test_device_status(
                device_type, device, event, is_update=True
            )

        check_device_control(device_type, device)

        logger.info(f"{device_type} Test with model : {model_name} is done.")
        cls.write_test_result(device_type, model_name, test_result)

    @classmethod
    @abc.abstractmethod
    def get_device_class(cls) -> type[ConnectBaseDevice]:
        pass

    @classmethod
    @abc.abstractmethod
    def get_device_type(cls) -> str:
        pass
