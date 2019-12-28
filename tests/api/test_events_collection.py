from chatovod.api.events_collection import EventNotRegisteredError, EventsCollection

import pytest


class TestEventsCollection:
    def test_register_class(self):
        collection = EventsCollection()

        @collection.register
        class BlankEvent:
            event_type = "blank"

        assert BlankEvent is not None
        assert len(collection.events_map) == 1
        assert collection.get_event_by_type("blank") == BlankEvent

    def test_get_event_by_type_raises_error_when_event_is_not_registered(self):
        collection = EventsCollection()

        with pytest.raises(EventNotRegisteredError):
            collection.get_event_by_type("invalid_event")
