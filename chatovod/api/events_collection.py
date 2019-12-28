API_EVENT_TYPE_ATTRIBUTE = "t"


class EventNotRegisteredError(Exception):
    """
    Error thrown when the requested event has not been registered in a collection.
    """


class BaseEvent:
    event_type: str = None
    new_type: int = None
    transforms: dict = None


class EventsCollection:
    def __init__(self):
        self.events_map = {}

    def register(self, event_structure: BaseEvent):
        self.events_map[event_structure.event_type] = event_structure

        return event_structure

    def get_event_by_type(self, event_type) -> BaseEvent:
        try:
            return self.events_map[event_type]
        except KeyError:
            raise EventNotRegisteredError(
                "The event {} is not registered is this collection".format(event_type)
            )
