#!/usr/bin/python3
"""
Defines the state model
"""
from .base_model import BaseModel


class Review(BaseModel):
    """
    Blueprint for Review objects
    """
    user_id = ""
    place_id = ""
    text = ""
