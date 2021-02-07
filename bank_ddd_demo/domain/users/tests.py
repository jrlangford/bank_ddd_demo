import uuid

from django.test import TestCase

from .models import *

class UserTests(TestCase):
    def test_validate_id(self):
        # Tests a valid ID
        id = uuid.uuid4()
        user = User(id = id)
        user.validate_id()

        id = 0xABAB
        user = User(id = id)
        with self.assertRaises(Exception):
            user.validate_id()

class UserFactoryTests(TestCase):
    def test_build(self):
        user = UserFactory.build_entity_with_id()
        user.validate_id()


