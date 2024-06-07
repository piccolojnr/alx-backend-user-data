#!/usr/bin/env python3
"""
Defines
"""
import uuid
from typing import TypeVar, Union
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    Session
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> Union[str, None]:
        """
        Create
        """
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id.update({session_id: user_id})
        return session_id

    def user_id_for_session_id(
        self,
        session_id: str = None,
    ) -> Union[str, None]:
        """
        Get user
        """
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None) -> Union[TypeVar("User"), None]:
        """
        Holds
        """
        User.load_from_file()
        u = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(u)

    def destroy_session(self, request=None) -> bool:
        """
        Deletes
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
