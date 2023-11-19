#!/usr/bin/python3
"""
Test suite for base_model
"""
import unittest
from models.base_model import BaseModel
from models.state import State


class TestBaseModel(unittest.TestCase):
    def test_attr(self):
        state = State()
        self.assertEqual(state.name, "")

    def test_parent(self):
        state = State()
        self.assertTrue(isinstance(state, BaseModel))
