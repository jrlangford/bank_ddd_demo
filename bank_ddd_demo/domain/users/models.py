import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    A User replaces django's default user id with a UUID that should be created by the application, not the database.
    """
    id = models.UUIDField(primary_key=True, editable=False)

    def validate_id(self):
        if uuid.UUID != type(self.id):
            raise Exception("The provided id is not a UUID")

    def check_invariants(self):
        self.validate_id()


class UserFactory():
    @staticmethod
    def build_entity_with_id():
        id = uuid.uuid4()
        return User(id=id)
