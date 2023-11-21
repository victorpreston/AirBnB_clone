#!/usr/bin/python3
"""
Class User that inherits from BaseModel
"""

from models.base_model import BaseModel


class User(BaseModel):
    """
    Blueprint for a User object
    Public Attributes that will use FileStorage in engine
    folder to manage serialization and deserialization of User
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
