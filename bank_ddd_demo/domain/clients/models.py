import uuid
from dataclasses import dataclass, asdict
from datetime import datetime

from django.db import models

from data_manipulation.type_conversion import asdict

class Client(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    first_transaction_date = models.DateTimeField(null=True)
    latest_transaction_date = models.DateTimeField(null=True)

    def validate_id(self):
        if uuid.UUID != type(self.id):
            raise Exception("The provided id is not a UUID")

    def check_invariants(self):
        self.validate_id()

@dataclass(frozen=True)
class ClientPlatformUsageData():
    """
    This is a value object that should be used to pass platform usage parameters to the ClientFactory
    Note: If we weren't using Django Models as entities we would be able to embed this object directly into the aggregate root.
    """
    first_transaction_date: datetime = None
    latest_transaction_date: datetime = None


class ClientFactory():
    @staticmethod
    def build_entity(id, usage_data: ClientPlatformUsageData):
        usage_data_dict = asdict(usage_data, skip_empty=True)
        client = Client(id=id, **usage_data_dict)
        client.check_invariants()
        return client
