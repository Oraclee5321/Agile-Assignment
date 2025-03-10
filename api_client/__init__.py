"""
API Client

[TODO]: Documentation


"""

import requests
from requests.auth import HTTPBasicAuth
from abc import ABC, abstractmethod
from enum import Enum, auto


class _InternalUserData:
    """
    Internal representation of user data.

    Marked internal **DO NOT** USE

    Exists solely as a struct for storing data temporarily before the server side database is created
    """

    def __init__(self, username, password):
        self.username = username
        # This is obviously stupid, its just temporary
        self.password = password

        self.coins = 0
        self.progression = None
        self.customisation = None
        self.badges = None
        self.scores = None
        self.daily_challenge_completed = False


class LoginStatus(Enum):
    INTERNAL_SERVER_ERROR = auto()
    NETWORK_ERROR = auto()
    SUCCESS = auto()
    INVALID_LOGIN = auto()
    ALREADY_LOGGED_IN = auto()

    # Potential statuses to be implemented serverside first
    # TOO_MANY_ATTEMPTS = auto()


class RegisterStatus(Enum):
    INTERNAL_SERVER_ERROR = auto()
    NETWORK_ERROR = auto()
    SUCCESS = auto()
    USERNAME_TAKEN = auto()

    # Potential statuses to be implemented serverside first
    # Currently no established rules on what can be a username and password
    # INVALID_USERNAME = auto()
    # INVALID_PASSWORD = auto()


class ApiClientInterface(ABC):
    """
    Interface for mock and real API clients.
    """

    @abstractmethod
    def logged_in(self) -> bool:
        """
        [TODO]: Documentation
        """

    @abstractmethod
    def login(self, username: str, password: str) -> LoginStatus:
        """
        [TODO]: Documentation
        """

    @abstractmethod
    def logout(self):
        """
        [TODO]: Documentation
        """

    @abstractmethod
    def register(self, username: str, password: str) -> RegisterStatus:
        """
        [TODO]: Documentation
        """

    @abstractmethod
    def get_username(self) -> str:
        pass

    @abstractmethod
    def get_coins(self) -> int:
        pass


class MockApiClient(ApiClientInterface):
    """
    API client that does not actually interact with the server.
    Exists for testing purposes to easily define the API behaivour
    and as a placeholder.
    """

    def __init__(self):
        # Currently just using a dictionary for data storage
        self.__users: dict[str, _InternalUserData] = {}
        self.__requests_session = requests.Session()
        # Temporary, just determines which user is logged in.
        # Replace later by creating an auth class inherited from
        # requests.Auth.AuthBase and use a JWT or something
        #
        # Dont do it in this class, make a seperate real ApiClient
        # class that interacts with server and ensure interface are the same.
        # Test against eeach other when testing them.
        self.__current_user: None | _InternalUserData = None

    def logged_in(self) -> bool:
        return self.__current_user is not None

    def login(self, username: str, password: str) -> LoginStatus:
        if self.logged_in():
            return LoginStatus.ALREADY_LOGGED_IN

        # Again, this is stupid. Its temporary
        user: _InternalUserData | None = self.__users.get(username)
        # if user exists and password is correct
        if user and user.password == password:
            self.__current_user = user
            return LoginStatus.SUCCESS
        else:
            return LoginStatus.INVALID_LOGIN

    def logout(self):
        self.__current_user = None

    def register(self, username: str, password: str) -> RegisterStatus:
        # If user does not exist
        if not self.__users.get(username, False):
            self.__users[username] = _InternalUserData(username, password)
            return RegisterStatus.SUCCESS
        else:
            return RegisterStatus.USERNAME_TAKEN

    def get_username(self) -> str:
        if self.__current_user is not None:
            return self.__current_user.username
        else:
            raise PermissionError

    def get_coins(self) -> int:
        if self.__current_user is not None:
            return self.__current_user.coins
        else:
            raise PermissionError
