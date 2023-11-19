#!/usr/bin/python3
"""
Test suite for base_model
"""
import unittest
from models.base_model import BaseModel
from models.review import Review


class TestBaseModel(unittest.TestCase):
    def test_str(self):
        review = Review()
        self.assertEqual(review.place_id, "")
        self.assertEqual(review.user_id, "")
        self.assertEqual(review.text, "")

    def test_parent(self):
        review = Review()
        self.assertTrue(isinstance(review, BaseModel))
