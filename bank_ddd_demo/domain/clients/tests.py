import uuid

from django.test import TestCase

from .models import *

# IMPORTANT: Note how we are able to test this module without accessing other domain modules

class ClientTests(TestCase):
    def test_validate_id(self):
        # Tests a valid ID
        id = uuid.uuid4()
        client = Client(id = id)
        client.validate_id()

        # Tests an invalid ID
        id = 0xABAB
        client = Client(id = id)
        with self.assertRaises(Exception):
            client.validate_id()

class ClientFactoryTests(TestCase):
    def test_create(self):
        id = uuid.uuid4()
        user = ClientFactory.create_entity(id)
        user.validate_id()
