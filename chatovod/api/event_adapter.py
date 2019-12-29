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


class EventAdapter:
    def __init__(self, events_collection: EventsCollection):
        self.events_collection = events_collection

    def transform(self, data, transforms):
        return {transforms.get(k, k): v for k, v in data.items()}

    def adapt(self, data: dict):
        event_type = data.get(API_EVENT_TYPE_ATTRIBUTE)
        event = self.events_collection.get_event_by_type(event_type)

        transformed_data = self.transform(data, event.transforms)

        # Patch the type of the event
        try:
            transformed_data[API_EVENT_TYPE_ATTRIBUTE] = event.new_type
        finally:
            return transformed_data
