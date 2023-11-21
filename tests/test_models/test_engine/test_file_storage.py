#!/usr/bin/python3
"""
Test suite for file_storage engine
"""
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.__init__ import storage


class TestFileStorage(unittest.TestCase):
    def test_private_attr(self):
        base = BaseModel()
        storage = FileStorage()
        with self.assertRaises(AttributeError):
            file_path = storage.file_path
        with self.assertRaises(AttributeError):
            file_path = storage.__file_path
        with self.assertRaises(AttributeError):
            file_path = storage.objects
        with self.assertRaises(AttributeError):
            file_path = storage.__objects

        with self.assertRaises(AttributeError):
            FileStorage.file_path
        with self.assertRaises(AttributeError):
            FileStorage.__file_path
        with self.assertRaises(AttributeError):
            FileStorage.objects
        with self.assertRaises(AttributeError):
            FileStorage.__objects

    def test_reload(self):
        storage1 = FileStorage()
        base1 = BaseModel({id: 8})
        base1.save()
        storage.save()
        self.assertEqual(storage.reload(), None)

    def test_a(self):
        storage1 = FileStorage()
        self.assertIsInstance(storage1.all(), dict)

    def test_b(self):
        storage1 = FileStorage()
        base = BaseModel()
        storage1.new(base)
        key = type(base).__name__ + '.' + base.id
        self.assertEqual(storage1.all()[key], base)

    """
    def test_a_all(self):
        all_objs = storage.all()
        self.assertDictEqual(storage.all(), {})

    def test_z_all(self):
        base = BaseModel()
        base.save()
        key = 'BaseModel.' + base.id
        self.assertIsInstance(storage.all(), dict)

    def test_reload(self):
        self.assertEqual(storage.reload(), None)
    """
