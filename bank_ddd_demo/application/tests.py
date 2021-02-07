from datetime import datetime
from decimal import Decimal

from django.test import TestCase

from bank_ddd_demo.domain.clients.services import ClientServices
from bank_ddd_demo.domain.users.services import UserServices
from bank_ddd_demo.domain.transactions.models import TransactionParams

from .services import ClientAppServices, TransactionAppServices

class ClientAppServiceTests(TestCase):
    # Note: Tests would not rely on DB  if save function were mocked
    def test_store_then_get_system_client(self):
        # Tests entity ids hold a value
        user, client = ClientAppServices.create_and_store_system_client()
        self.assertNotEquals(user.id, None)
        self.assertNotEquals(client.id, None)

        # Tests entities are saved to DB
        db_user = ClientServices.get_client_repo().get(id=client.id)
        db_client = ClientServices.get_client_repo().get(id=client.id)
        self.assertNotEquals(db_user, None)
        self.assertNotEquals(db_client, None)

    def test_get_client_from_user(self):
        user, client = ClientAppServices.create_and_store_system_client()

        try:
            client = ClientAppServices.get_client_from_user(user)
        except:
            self.fail("Unexpected exception!")

        with self.assertRaises(Exception):
            dummyUser = None
            client = ClientAppServices.get_client_from_user(dummyUser)


class TransactionAppServicesTests(TestCase):
    # Note: Tests would not rely on DB  if save function were mocked
    def test_store_then_get_transaction(self):
        user, client = ClientAppServices.create_and_store_system_client()

        # Tests a client can perform a transaction
        t = TransactionParams(
            client_id = client.id,
            submission_datetime = datetime.now(),
            amount = Decimal("12435.678"),
        )

        try:
            transaction = TransactionAppServices.create_and_store_transaction(client, t)
        except:
            self.fail("Unexpected exception!")

        # Tests a (system) user can register a transaction on the client's behalf
        another_user = UserServices.get_user_factory().create_entity_with_id()
        try:
            transaction = TransactionAppServices.create_and_store_transaction(user, t)
        except:
            self.fail("Unexpected exception!")
