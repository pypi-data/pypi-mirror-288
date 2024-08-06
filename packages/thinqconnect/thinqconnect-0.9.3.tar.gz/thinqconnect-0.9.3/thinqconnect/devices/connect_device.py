from __future__ import annotations

from collections import defaultdict
from typing import Any

from ..const import PROPERTY_READABLE, PROPERTY_WRITABLE
from ..device import BaseDevice
from ..thinq_api import ThinQApi, ThinQApiResponse

TYPE = "type"
UNIT = "unit"
READABILITY = "readable"
WRITABILITY = "writable"
READABLE_VALUES = "read_values"
WRITABLE_VALUES = "write_values"


class ConnectDeviceProfile:
    _RESOURCE_MAP: dict[str, str] = {}
    _LOCATION_MAP: dict[str, str] = {}
    _PROFILE: dict[str, dict[str, str]] = {}
    _CUSTOM_RESOURCES: list[str] = []

    def __init__(
        self, profile: dict[str, Any], use_extension_property: bool = False, use_sub_profile_only: bool = False
    ):
        self._properties: dict[str, list] = {}
        self._location_properties: dict[str, dict[str, list]] = {}

        if not use_sub_profile_only:
            self.generate_errors(errors=profile.get("error"))
            self.generate_notification(notification=profile.get("notification"))
            self.generate_properties(
                property=profile.get("property" if not use_extension_property else "extensionProperty")
            )
        else:
            self._errors = None
            self._notification = None

    @staticmethod
    def _safe_get(data, *keys):
        for key in keys:
            try:
                data = data[key]
            except (TypeError, KeyError):
                return None
        return data

    @staticmethod
    def _is_readable_property(property: Any) -> bool:
        return (not isinstance(property, dict)) or "r" in property.get("mode", [])

    @staticmethod
    def _is_writable_property(property: Any) -> bool:
        return isinstance(property, dict) and "w" in property.get("mode", [])

    @staticmethod
    def __disable_prop_mode_value(type: str) -> dict | list:
        return {} if type == "range" else []

    @staticmethod
    def _get_properties(resource_property: dict, key: str) -> dict:
        _property: str | dict[str:Any] = resource_property.get(key, {})
        if isinstance(_property, str):
            return {
                TYPE: "string",
                READABILITY: True,
                WRITABILITY: False,
                READABLE_VALUES: [_property],
                WRITABLE_VALUES: [],
            }

        _property_type = _property.get(TYPE)
        _property_unit = _property.get(UNIT) or resource_property.get(UNIT)
        prop = {
            TYPE: _property_type,
            READABILITY: ConnectDeviceProfile._is_readable_property(_property),
            WRITABILITY: ConnectDeviceProfile._is_writable_property(_property),
            **({UNIT: _property_unit} if _property_unit else {}),
        }
        if isinstance(_property, dict) and _property_type in ["enum", "range", "list"]:
            prop[READABLE_VALUES] = (
                ConnectDeviceProfile._safe_get(resource_property, key, "value", PROPERTY_READABLE)
                if prop[READABILITY]
                else ConnectDeviceProfile.__disable_prop_mode_value(_property_type)
            )
            prop[WRITABLE_VALUES] = (
                ConnectDeviceProfile._safe_get(resource_property, key, "value", PROPERTY_WRITABLE)
                if prop[WRITABILITY]
                else ConnectDeviceProfile.__disable_prop_mode_value(_property_type)
            )
        return prop

    @property
    def properties(self) -> dict:
        return self._properties

    @property
    def location_properties(self) -> dict:
        return self._location_properties

    @property
    def writable_properties(self) -> list:
        _writable_props = []
        for resource in self.properties.keys():
            _writable_props.extend(getattr(self, resource)["w"])
        return _writable_props

    @property
    def notification(self) -> dict | None:
        return self._notification

    @property
    def errors(self) -> list | None:
        return self._errors

    @property
    def locations(self):
        return self._location_properties.keys()

    def get_sub_profile(self, location_name: str) -> ConnectDeviceProfile | None:
        if location_name in self.locations:
            return getattr(self, location_name)
        else:
            return None

    def get_location_key(self, location_name: str) -> str | None:
        for key, name in self._LOCATION_MAP.items():
            if name == location_name:
                return key

    def get_property(self, property_name: str) -> dict:
        _prop = self._get_prop_attr(property_name)
        if _prop.get(READABLE_VALUES) or _prop.get(WRITABLE_VALUES):
            return {
                TYPE: _prop[TYPE],
                PROPERTY_READABLE: _prop[READABLE_VALUES],
                PROPERTY_WRITABLE: _prop[WRITABLE_VALUES],
                **({UNIT: _prop[UNIT]} if _prop.get(UNIT) else {}),
            }
        return {TYPE: _prop[TYPE], PROPERTY_READABLE: _prop[READABILITY], PROPERTY_WRITABLE: _prop[WRITABILITY]}

    def get_profile(self) -> dict:
        return self._PROFILE

    def generate_errors(self, errors: list[str] | None) -> None:
        self._errors = errors if errors else None

    def generate_notification(self, notification: dict[str, Any] | None) -> None:
        self._notification = notification if notification else None

    def _get_prop_attr(self, key: str) -> dict:
        return getattr(self, f"__{key}")

    def _set_prop_attr(self, key: str, prop: dict) -> None:
        setattr(self, f"__{key}", prop)

    def _generate_custom_resource_properties(
        self, resource_key: str, resource_property: dict | list, props: dict[str, str]
    ) -> tuple[list[str], list[str]]:
        # pylint: disable=unused-argument
        readable_props = []
        writable_props = []
        # Need to be implemented by child classes
        return readable_props, writable_props

    def _generate_resource_properties(
        self, resource_property: dict | list, props: dict[str, str]
    ) -> tuple[list[str], list[str]]:
        readable_props = []
        writable_props = []

        for prop_key, prop_attr in props.items():
            prop = self._get_properties(resource_property, prop_key)
            if prop[READABILITY]:
                readable_props.append(prop_attr)
            if prop[WRITABILITY]:
                writable_props.append(prop_attr)
            self._set_prop_attr(prop_attr, prop)
        return readable_props, writable_props

    def generate_properties(self, property: dict[str, Any]) -> None:
        """Get properties."""
        _properties = {}
        for resource, props in self._PROFILE.items():
            resource_property = property.get(resource)
            _readable = None
            _writable = None
            if resource_property:
                if resource in self._CUSTOM_RESOURCES:
                    _readable, _writable = self._generate_custom_resource_properties(
                        resource, resource_property, props
                    )
                elif isinstance(resource_property, dict):
                    _readable, _writable = self._generate_resource_properties(resource_property, props)
                readable_list = _readable or []
                writable_list = _writable or []
                if readable_list or writable_list:
                    _properties[self._RESOURCE_MAP[resource]] = list(set(readable_list + writable_list))
                setattr(self, self._RESOURCE_MAP[resource], {"r": _readable, "w": _writable})
            else:
                setattr(self, self._RESOURCE_MAP[resource], None)
                for _, prop_attr in props.items():
                    self._set_prop_attr(prop_attr, {READABILITY: False, WRITABILITY: False})

        setattr(self, "_properties", _properties)

    def check_attribute_readable(self, prop_attr: str) -> bool:
        return self._get_prop_attr(prop_attr)[READABILITY]

    def check_attribute_writable(self, prop_attr: str) -> bool:
        return self._get_prop_attr(prop_attr)[WRITABILITY]

    def check_range_attribute_writable(self, prop_attr: str, value: int) -> bool:
        values = self._get_prop_attr(prop_attr)[WRITABLE_VALUES]
        if not values:
            return False
        v_min = values["min"]
        v_max = values["max"]
        v_step = values.get("step", 1)
        v_except = values.get("except", [])
        return v_min <= value and value <= v_max and (value - v_min) % v_step == 0 and value not in v_except

    def check_enum_attribute_writable(self, prop_attr: str, value: str | bool) -> bool:
        return self._get_prop_attr(prop_attr)[WRITABILITY] and value in self._get_prop_attr(prop_attr)[WRITABLE_VALUES]

    def _get_attribute_payload(self, attribute: str, value: str | int) -> dict:
        for resource, props in self._PROFILE.items():
            for prop_key, prop_attr in props.items():
                if prop_attr == attribute:
                    return {resource: {prop_key: value}}

    def get_attribute_payload(self, attribute: str, value: int | bool) -> dict:
        if not self.check_attribute_writable(attribute):
            raise ValueError(f"Not support {attribute}")
        return self._get_attribute_payload(attribute, value)

    def get_range_attribute_payload(self, attribute: str, value: int) -> dict:
        if not self.check_range_attribute_writable(attribute, value):
            raise ValueError(f"Not support {attribute}")
        return self._get_attribute_payload(attribute, value)

    def get_enum_attribute_payload(self, attribute: str, value: str) -> dict:
        if not self.check_enum_attribute_writable(attribute, value):
            raise ValueError(f"Not support {attribute} : {value}")
        return self._get_attribute_payload(attribute, value)


class ConnectBaseDevice(BaseDevice):
    _CUSTOM_SET_PROPERTY_NAME = {}

    def __init__(
        self,
        thinq_api: ThinQApi,
        device_id: str,
        device_type: str,
        model_name: str,
        alias: str,
        reportable: bool,
        profiles: ConnectDeviceProfile,
    ):
        super().__init__(
            thinq_api=thinq_api,
            device_id=device_id,
            device_type=device_type,
            model_name=model_name,
            alias=alias,
            reportable=reportable,
        )
        self._profiles: ConnectDeviceProfile = profiles
        self._sub_devices: dict[str, ConnectBaseDevice] = {}

    @property
    def profiles(self) -> ConnectDeviceProfile:
        return self._profiles

    def get_property_keys(self, resource: str, origin_keys: list[str]) -> list[str | None]:
        _resource_profile: dict[str, str] = self.profiles.get_profile().get(resource, {})

        return [_resource_profile.get(origin_key, None) for origin_key in origin_keys]

    def __return_exist_fun_name(self, fn_name: str) -> str | None:
        return fn_name if hasattr(self, fn_name) else None

    def get_property_set_fn(self, property_name: str) -> str | None:
        return (
            self.__return_exist_fun_name(f"set_{property_name}")
            if property_name not in self._CUSTOM_SET_PROPERTY_NAME
            else self.__return_exist_fun_name(f"set_{self._CUSTOM_SET_PROPERTY_NAME[property_name]}")
        )

    def get_sub_device(self, location_name: str) -> ConnectBaseDevice | None:
        if location_name in self.profiles.locations:
            return self._sub_devices.get(location_name)
        else:
            return None

    def _set_custom_resources(self, attribute: str, resource_status: dict[str, str] | list[dict[str, str]]) -> bool:
        # pylint: disable=unused-argument
        # Need to be implemented by child classes
        return False

    def __set_property_status(
        self, resource_status: dict | None, resource: str, prop_key: str, prop_attr: str, is_updated: bool = False
    ) -> None:
        if prop_attr == "location_name":
            return

        value = None
        if resource_status is not None:
            if resource in self.profiles._CUSTOM_RESOURCES:
                if self._set_custom_resources(prop_attr, resource_status):
                    return
            if isinstance(resource_status, dict):
                value = resource_status.get(prop_key)
            if is_updated:
                if prop_key in resource_status:
                    self._set_status_attr(prop_attr, value)
                return

        self._set_status_attr(prop_attr, value)

    def _set_status_attr(self, property_name: str, value: Any) -> None:
        setattr(self, property_name, value)

    def __set_error_status(self, status: dict) -> None:
        if self.profiles.errors:
            self._set_status_attr("error", status.get("error"))

    def __set_status(self, status: dict) -> None:
        for resource, props in self.profiles.get_profile().items():
            resource_status = status.get(resource)
            for prop_key, prop_attr in props.items():
                self.__set_property_status(resource_status, resource, prop_key, prop_attr)

    def __update_status(self, status: dict) -> None:
        device_profile = self.profiles.get_profile()
        for resource, resource_status in status.items():
            if resource not in device_profile:
                continue
            for prop_key, prop_attr in device_profile[resource].items():
                self.__set_property_status(resource_status, resource, prop_key, prop_attr, True)

    def _set_status(self, status: dict | list, is_updated: bool = False) -> None:
        if not isinstance(status, dict):
            return
        self.__set_error_status(status)
        if is_updated:
            self.__update_status(status)
        else:
            self.__set_status(status)

    def get_status(self, property_name: str) -> Any:
        return (
            getattr(self, property_name)
            if hasattr(self, property_name)
            and (property_name == "error" or self.profiles.check_attribute_readable(property_name))
            else None
        )

    def set_status(self, status: dict | list) -> None:
        self._set_status(status)

    def update_status(self, status: dict | list) -> None:
        self._set_status(status, True)

    async def _do_attribute_command(self, payload: dict) -> ThinQApiResponse:
        return await self.thinq_api.async_post_device_control(device_id=self.device_id, payload=payload)

    async def do_attribute_command(self, attribute: str, value: int | bool) -> ThinQApiResponse:
        return await self._do_attribute_command(self.profiles.get_attribute_payload(attribute, value))

    async def do_multi_attribute_command(self, attributes: dict[str, int]) -> ThinQApiResponse:
        payload = defaultdict(dict)
        for attr, value in attributes.items():
            for key, sub_dict in self.profiles.get_attribute_payload(attr, value).items():
                payload[key].update(sub_dict)
        return await self._do_attribute_command(payload)

    async def do_range_attribute_command(self, attribute: str, value: int) -> ThinQApiResponse:
        return await self._do_attribute_command(self.profiles.get_range_attribute_payload(attribute, value))

    async def do_multi_range_attribute_command(self, attributes: dict[str, int]) -> ThinQApiResponse:
        payload = defaultdict(dict)
        for attr, value in attributes.items():
            for key, sub_dict in self.profiles.get_range_attribute_payload(attr, value).items():
                payload[key].update(sub_dict)
        return await self._do_attribute_command(payload)

    async def do_enum_attribute_command(self, attribute: str, value: str) -> ThinQApiResponse:
        return await self._do_attribute_command(self.profiles.get_enum_attribute_payload(attribute, value))


class ConnectMainDevice(ConnectBaseDevice):
    def __init__(
        self,
        thinq_api: ThinQApi,
        device_id: str,
        device_type: str,
        model_name: str,
        alias: str,
        reportable: bool,
        profiles: ConnectDeviceProfile,
        sub_device_type: type,
    ):
        super().__init__(
            thinq_api=thinq_api,
            device_id=device_id,
            device_type=device_type,
            model_name=model_name,
            alias=alias,
            reportable=reportable,
            profiles=profiles,
        )
        self._sub_devices: dict[str, ConnectSubDevice] = {}
        for location_name in self.profiles.locations:
            _sub_device = sub_device_type(
                profiles=self.profiles.get_sub_profile(location_name),
                location_name=self.profiles.get_location_key(location_name),
                thinq_api=thinq_api,
                device_id=device_id,
                device_type=device_type,
                model_name=model_name,
                alias=alias,
                reportable=reportable,
            )
            setattr(self, location_name, _sub_device)
            self._sub_devices[location_name] = _sub_device

    def set_status(self, status: list) -> None:
        super().set_status(status)
        for sub_device in self._sub_devices.values():
            sub_device.set_status(status)

    def update_status(self, status: list) -> None:
        super().update_status(status)
        for sub_device in self._sub_devices.values():
            sub_device.update_status(status)


class ConnectSubDevice(ConnectBaseDevice):
    def __init__(
        self,
        profiles: ConnectDeviceProfile,
        location_name: str,
        thinq_api: ThinQApi,
        device_id: str,
        device_type: str,
        model_name: str,
        alias: str,
        reportable: bool,
        is_single_resource: bool = False,
    ):
        super().__init__(thinq_api, device_id, device_type, model_name, alias, reportable, profiles)
        self._location_name = location_name
        self._is_single_resource = is_single_resource

    @property
    def location_name(self) -> str:
        return self._location_name

    def _get_location_name_from_status(self, location_status: dict) -> str | None:
        if self._is_single_resource:
            return location_status.get("locationName")
        else:
            return location_status.get("location", {}).get("locationName")

    def _is_current_location_status(self, location_status: dict) -> bool:
        return self._get_location_name_from_status(location_status) == self._location_name

    def _set_status(self, status: list | dict, is_updated: bool = False) -> None:
        if isinstance(status, list):
            for location_status in status:
                if not self._is_current_location_status(location_status):
                    continue
                super()._set_status(status=location_status, is_updated=is_updated)
                return
            return
        for resource in self.profiles._CUSTOM_RESOURCES:
            for location_status in status.get(resource, []):
                if not self._is_current_location_status(location_status):
                    continue
                super()._set_status(status={resource: location_status}, is_updated=is_updated)
                return
