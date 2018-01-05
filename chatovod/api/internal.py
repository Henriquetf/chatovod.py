from chatovod.api.http import HTTPClient


class InternalState:

    def __init__(self, *, client):
        self.client = client
        self.http = HTTPClient()
