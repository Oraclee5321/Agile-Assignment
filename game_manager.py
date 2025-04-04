from api_client import ApiClientInterface, MockApiClient, AuthResponse


class GameManager:
    def __init__(self, api_client: ApiClientInterface) -> None:
        # currently just encapsulates api_client but will add
        # settings to it later
        self.api_client = api_client
