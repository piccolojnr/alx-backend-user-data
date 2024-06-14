#!/usr/bin/env python3
"""_summary_
"""
from db import DB
from user import User

import bcrypt
from uuid import uuid4 as uuid

from typing import Union

from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash the given password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def _generate_uuid() -> str:
    return str(uuid())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Validate a login"""
        user = self._db.find_user_by(email=email)
        return bcrypt.checkpw(password.encode(), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Create a session"""
        user = self._db.find_user_by(email=email)
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """_summary_

        Args:
            session_id (str): _description_

        Returns:
            Union[User, None]: _description_
        """
        user = self._db.find_user_by(session_id=session_id)
        return user

    def destroy_session(self, user_id: int) -> None:
        """_summary_

        Args:
            user_id (int): _description_
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """_summary_

        Args:
            email (str): _description_

        Returns:
            str: _description_
        """
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError(f"User {email} doesn't exist")
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """_summary_

        Args:
            reset_token (str): _description_
            password (str): _description_
        """
        user = self._db.find_user_by(reset_token=reset_token)
        if not user:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=hashed_password,
            reset_token=None,
        )
        return None
