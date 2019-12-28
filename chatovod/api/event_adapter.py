from .events_collection import API_EVENT_TYPE_ATTRIBUTE, EventsCollection


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
