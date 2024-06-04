#!/usr/bin/env python3
"""manage the API authentication.
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """basic auth

    Args:
        Auth (_type_): _description_
    """

    def extract_base64_authorization_header(
        self,
        authorization_header: str,
    ) -> str:
        """extract base64 authorization header

        Args:
            authorization_header (str): header

        Returns:
            str: base64 string
        """
        if authorization_header is None or type(authorization_header) != str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """decode base64 authorization header

        Args:
            base64_authorization_header (str): base64 string

        Returns:
            str: decoded string
        """
        if (
            base64_authorization_header is None
            or type(base64_authorization_header) != str
        ):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """extract credentials

        Args:
            decoded_base64_authorization_header (str): decoded string

        Returns:
            (str, str): tuple of credentials
        """
        if (
            decoded_base64_authorization_header is None
            or type(decoded_base64_authorization_header) != str
            or ":" not in decoded_base64_authorization_header
        ):
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(":", 1))

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """user object from credentials

        Args:
            user_email (str): email
            user_pwd (str): password

        Returns:
            TypeVar('User'): user object
        """
        if (
            user_email is None
            or type(user_email) != str
            or user_pwd is None
            or type(user_pwd) != str
        ):
            return None
        User.load_from_file()
        if User.count > 0:
            user_list = User.search({"email": user_email})
            for user in user_list:
                if user.is_valid_password(user_pwd):
                    return user
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """current user"""
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        if b64_auth_header is None:
            return None
        decoded_b64_auth_header = self.decode_base64_authorization_header(
            b64_auth_header
        )
        if decoded_b64_auth_header is None:
            return None
        data = self.extract_user_credentials(decoded_b64_auth_header)
        user_email, user_pwd = data
        if user_email is None or user_pwd is None:
            return None
        return self.user_object_from_credentials(user_email, user_pwd)
