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
        personal_data = UserPersonalData(
            username = "Tester",
            first_name = "Testerman",
            last_name = "Testerson",
            email = "testerman@example.com"
        )
        base_permissions = UserBasePermissions(
            is_staff = False,
            is_active = False
        )
        user = UserFactory.build_entity_with_id(personal_data, base_permissions)
        user.validate_id()


