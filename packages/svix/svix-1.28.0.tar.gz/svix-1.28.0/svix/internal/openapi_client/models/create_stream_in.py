from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.event_in import EventIn


T = TypeVar("T", bound="CreateStreamIn")


@attr.s(auto_attribs=True)
class CreateStreamIn:
    """
    Attributes:
        events (List['EventIn']):
    """

    events: List["EventIn"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        events = []
        for events_item_data in self.events:
            events_item = events_item_data.to_dict()

            events.append(events_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "events": events,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.event_in import EventIn

        d = src_dict.copy()
        events = []
        _events = d.pop("events")
        for events_item_data in _events:
            events_item = EventIn.from_dict(events_item_data)

            events.append(events_item)

        create_stream_in = cls(
            events=events,
        )

        create_stream_in.additional_properties = d
        return create_stream_in

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
