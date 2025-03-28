"""
API Client

[TODO]: Documentation


"""

import requests
from requests.auth import HTTPBasicAuth
from abc import ABC, abstractmethod
from enum import Enum, auto
from dataclasses import dataclass


class GameScore:
    pass


class Badge:
    # Or should i just have BadgeData that contains the info
    # What does a badge need:
    #   progress % float
    #   completion bool
    #   name str
    #   description str
    pass


class _InternalUserData:
    """
    Internal representation of user data.

    Marked internal **DO NOT** USE

    Exists solely as a struct for storing data temporarily before the server side database is created
    """

    def __init__(self, username, password):
        self.username: str = username
        # This is obviously stupid, its just temporary
        self.password: str = password

        self.coins: int = 0
        self.progression = None
        self.badges = dict[str, Badge]
        self.game_scores: dict[str, GameScore] = {}
        # self.daily_challenge_completed = False


@dataclass
class AuthResponse:
    success: bool
    message: str | None = None


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
    def login(self, username: str, password: str) -> AuthResponse:
        """
        [TODO]: Documentation
        """

    @abstractmethod
    def logout(self):
        """
        [TODO]: Documentation
        """

    @abstractmethod
    def register(self, username: str, password: str) -> AuthResponse:
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
        # Temporary, just determines which user is logged in.
        # Replace later by creating an auth class inherited from
        # requests.Auth.AuthBase and use a JWT or something
        # Dont do it in this class, make a seperate real ApiClient
        # class that interacts with server and ensure interface are the same.
        # Test against eeach other when testing them.
        self.__current_user: None | _InternalUserData = None

    def logged_in(self) -> bool:
        return self.__current_user is not None

    def login(self, username: str, password: str) -> AuthResponse:
        if self.__current_user is not None:
            return AuthResponse(False, "User already logged in")

        # Again, this is stupid. Its temporary
        user: _InternalUserData | None = self.__users.get(username)
        # if user exists and password is correct
        if user and user.password == password:
            self.__current_user = user
            return AuthResponse(True)
        else:
            return AuthResponse(False, "Invalid credentials")

    def logout(self):
        self.__current_user = None

    def register(self, username: str, password: str) -> AuthResponse:
        # If user does not exist
        if len(username) < 4:
            return AuthResponse(False, "Username must be above 4 characters")
        if len(password) < 4:
            return AuthResponse(False, "Password must be above 4 characters")

        if not self.__users.get(username, False):
            self.__users[username] = _InternalUserData(username, password)
            return AuthResponse(True)
        else:
            return AuthResponse(False, "Username taken")

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

    def add_coins(self, coins: int):
        if self.__current_user is not None:
            self.__current_user.coins += coins
        else:
            raise PermissionError
