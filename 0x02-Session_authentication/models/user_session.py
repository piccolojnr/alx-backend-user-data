#!/usr/bin/env python3
"""
UserSession class
"""
from datetime import datetime

from models.base import Base


class UserSession(Base):
    """
    session class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Instialize
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
        self.created_at = datetime.now()
