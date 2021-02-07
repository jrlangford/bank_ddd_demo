import uuid

from django.db import models

class Client(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    first_transaction_date = models.DateTimeField(null=True)
    latest_transaction_date = models.DateTimeField(null=True)

    def validate_id(self):
        if uuid.UUID != type(self.id):
            raise Exception("The provided id is not a UUID")

    def check_invariants(self):
        self.validate_id()

class ClientFactory():
    @staticmethod
    def build_entity(id):
        client = Client(id=id)
        client.check_invariants()
        return client
