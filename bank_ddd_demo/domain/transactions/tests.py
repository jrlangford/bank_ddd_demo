import uuid
from decimal import Decimal
import dataclasses

from django.test import TestCase

from .models import *

# IMPORTANT: Note how we are able to test this module without accessing other domain modules

class TransactionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.transaction_id_01 = uuid.uuid4()

    def test_validate_id(self):
        # Tests a valid ID
        id = self.transaction_id_01
        transaction = Transaction(id = id)
        transaction.validate_id()

        # Tests an invalid ID
        id = 0xABAB
        transaction = Transaction(id = id)
        with self.assertRaises(Exception):
            transaction.validate_id()


class TransactionFactoryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.transaction_data = {
            'client_id': uuid.uuid4(),
            'submission_datetime':  datetime.now(),
            'amount': Decimal("12435.678"),
        }

    def test_set_params(self):
        t = None
        try:
            t = TransactionParams(**self.transaction_data)
        except:
            self.fail("Unexpected exception!")

        with self.assertRaises(Exception):
            cls.bad_transaction_params_01 = dataclasses.replace(t, client_id = 0xFAFAFA)

    def test_build_entity_with_id(self):
        t = TransactionParams(**self.transaction_data)
        transaction = TransactionFactory.build_entity_with_id(t)
        transaction.check_invariants()
