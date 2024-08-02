from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.canvas_initialize_webhook_v0_type import CanvasInitializeWebhookV0Type
from ..types import UNSET, Unset

T = TypeVar("T", bound="CanvasInitializeWebhookV0")


@attr.s(auto_attribs=True, repr=False)
class CanvasInitializeWebhookV0:
    """Sent when a user initializes a canvas via trigger in the Benchling UI.
    Please migrate to CanvasInitializeWebhookV2."""

    _feature_id: str
    _resource_id: str
    _type: CanvasInitializeWebhookV0Type
    _deprecated: bool
    _excluded_properties: List[str]

    def __repr__(self):
        fields = []
        fields.append("feature_id={}".format(repr(self._feature_id)))
        fields.append("resource_id={}".format(repr(self._resource_id)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("deprecated={}".format(repr(self._deprecated)))
        fields.append("excluded_properties={}".format(repr(self._excluded_properties)))
        return "CanvasInitializeWebhookV0({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        feature_id = self._feature_id
        resource_id = self._resource_id
        type = self._type.value

        deprecated = self._deprecated
        excluded_properties = self._excluded_properties

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if feature_id is not UNSET:
            field_dict["featureId"] = feature_id
        if resource_id is not UNSET:
            field_dict["resourceId"] = resource_id
        if type is not UNSET:
            field_dict["type"] = type
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated
        if excluded_properties is not UNSET:
            field_dict["excludedProperties"] = excluded_properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_feature_id() -> str:
            feature_id = d.pop("featureId")
            return feature_id

        try:
            feature_id = get_feature_id()
        except KeyError:
            if strict:
                raise
            feature_id = cast(str, UNSET)

        def get_resource_id() -> str:
            resource_id = d.pop("resourceId")
            return resource_id

        try:
            resource_id = get_resource_id()
        except KeyError:
            if strict:
                raise
            resource_id = cast(str, UNSET)

        def get_type() -> CanvasInitializeWebhookV0Type:
            _type = d.pop("type")
            try:
                type = CanvasInitializeWebhookV0Type(_type)
            except ValueError:
                type = CanvasInitializeWebhookV0Type.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(CanvasInitializeWebhookV0Type, UNSET)

        def get_deprecated() -> bool:
            deprecated = d.pop("deprecated")
            return deprecated

        try:
            deprecated = get_deprecated()
        except KeyError:
            if strict:
                raise
            deprecated = cast(bool, UNSET)

        def get_excluded_properties() -> List[str]:
            excluded_properties = cast(List[str], d.pop("excludedProperties"))

            return excluded_properties

        try:
            excluded_properties = get_excluded_properties()
        except KeyError:
            if strict:
                raise
            excluded_properties = cast(List[str], UNSET)

        canvas_initialize_webhook_v0 = cls(
            feature_id=feature_id,
            resource_id=resource_id,
            type=type,
            deprecated=deprecated,
            excluded_properties=excluded_properties,
        )

        return canvas_initialize_webhook_v0

    @property
    def feature_id(self) -> str:
        if isinstance(self._feature_id, Unset):
            raise NotPresentError(self, "feature_id")
        return self._feature_id

    @feature_id.setter
    def feature_id(self, value: str) -> None:
        self._feature_id = value

    @property
    def resource_id(self) -> str:
        if isinstance(self._resource_id, Unset):
            raise NotPresentError(self, "resource_id")
        return self._resource_id

    @resource_id.setter
    def resource_id(self, value: str) -> None:
        self._resource_id = value

    @property
    def type(self) -> CanvasInitializeWebhookV0Type:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: CanvasInitializeWebhookV0Type) -> None:
        self._type = value

    @property
    def deprecated(self) -> bool:
        if isinstance(self._deprecated, Unset):
            raise NotPresentError(self, "deprecated")
        return self._deprecated

    @deprecated.setter
    def deprecated(self, value: bool) -> None:
        self._deprecated = value

    @property
    def excluded_properties(self) -> List[str]:
        """These properties have been dropped from the payload due to size."""
        if isinstance(self._excluded_properties, Unset):
            raise NotPresentError(self, "excluded_properties")
        return self._excluded_properties

    @excluded_properties.setter
    def excluded_properties(self, value: List[str]) -> None:
        self._excluded_properties = value
