from datetime import datetime
from decimal import Decimal

from django.test import TestCase

from bank_ddd_demo.domain.users.models import UserPersonalData, UserBasePermissions

from bank_ddd_demo.domain.clients.services import ClientServices
from bank_ddd_demo.domain.users.services import UserServices
from bank_ddd_demo.domain.transactions.models import TransactionParams

from .services import ClientAppServices, TransactionAppServices

class ClientAppServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.personal_data_01 = UserPersonalData(
            username = "Tester",
            first_name = "Testerman",
            last_name = "Testerson",
            email = "testerman@example.com"
        )
        cls.base_permissions_01 = UserBasePermissions(
            is_staff = False,
            is_active = False
        )
    # Note: Tests would not rely on DB  if save function were mocked
    def test_store_then_get_system_client(self):
        # Tests entity ids hold a value
        user, client = ClientAppServices.create_system_client(self.personal_data_01, self.base_permissions_01)
        self.assertNotEquals(user.id, None)
        self.assertNotEquals(client.id, None)

        # Tests entities are saved to DB
        db_user = ClientServices.get_client_repo().get(id=client.id)
        db_client = ClientServices.get_client_repo().get(id=client.id)
        self.assertNotEquals(db_user, None)
        self.assertNotEquals(db_client, None)

    def test_get_client_from_user(self):
        user, client = ClientAppServices.create_system_client(self.personal_data_01, self.base_permissions_01)

        try:
            client = ClientAppServices.get_client_from_user(user)
        except:
            self.fail("Unexpected exception!")

        with self.assertRaises(Exception):
            dummyUser = None
            client = ClientAppServices.get_client_from_user(dummyUser)


class TransactionAppServicesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.personal_data_01 = UserPersonalData(
            username = "Tester",
            first_name = "Testerman",
            last_name = "Testerson",
            email = "testerman@example.com"
        )
        cls.base_permissions_01 = UserBasePermissions(
            is_staff = False,
            is_active = False
        )

        cls.personal_data_02 = UserPersonalData(
            username = "Tester2",
            first_name = "Testerman2",
            last_name = "Testerson2",
            email = "testerman2@example.com"
        )
        cls.base_permissions_02 = UserBasePermissions(
            is_staff = False,
            is_active = False
        )

    # Note: Tests would not rely on DB  if save function were mocked
    def test_create_transaction(self):
        user, client = ClientAppServices.create_system_client(self.personal_data_01, self.base_permissions_01)

        # Tests a client can perform a transaction
        t = TransactionParams(
            client_id = client.id,
            submission_datetime = datetime.now(),
            amount = Decimal("12435.678"),
        )

        try:
            transaction = TransactionAppServices.create_transaction(client, t)
        except:
            self.fail("Unexpected exception!")

        # Tests a (system) user can register a transaction on the client's behalf
        another_user = UserServices.get_user_factory().build_entity_with_id(self.personal_data_01, self.base_permissions_01)
        try:
            transaction = TransactionAppServices.create_transaction(user, t)
        except:
            self.fail("Unexpected exception!")
