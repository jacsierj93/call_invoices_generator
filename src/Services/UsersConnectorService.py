from fastapi import HTTPException
import requests
import os

from src.Dto.Models import UserResponse

class UsersConnectorService:
    """
    A service class to interact with the Users API.

    Attributes:
        _url (str): The base URL for the Users API, fetched from the environment variable `USERS_API_URL`.
    """
    _url = None

    def __init__(self):
        """
        Initializes the UsersConnectorService by setting the base URL for the Users API.
        """
        self._url = os.environ.get("USERS_API_URL")

    def get_user(self, phone: str) -> UserResponse:
        """
        Fetches user details from the Users API using the provided phone number.

        Args:
            phone (str): The phone number of the user to fetch.

        Returns:
            UserResponse: A UserResponse object containing the user's details.

        Raises:
            HTTPException: If the user is not found (HTTP 404).
        """
        response = requests.get(self._url.replace(":phoneNumber", phone))
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(**response.json())