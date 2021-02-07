import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from decimal import Decimal
from typing import Tuple, ClassVar

from django.db import models

from data_manipulation.type_conversion import asdict


class Transaction(models.Model):

    DEPOSIT = 'D'
    WITHDRAWAL = 'W'
    TYPE_CHOICES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
    ]


    id = models.UUIDField(primary_key=True, editable=False)
    client_id = models.UUIDField(null=False)

    submission_datetime = models.DateTimeField()
    transaction_type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES
    )
    amount = models.DecimalField(max_digits=40, decimal_places=20)


    def validate_id(self):
        if uuid.UUID != type(self.id):
            raise Exception("The provided id is not a UUID")

    def check_invariants(self):
        self.validate_id()


@dataclass(frozen=True)
class TransactionWarning():
    code: int
    message: str


@dataclass(frozen=True)
class TransactionParams():
    """
    This is a value object that should be used to pass transaction parameters to the TransactionFactory
    Note: If we weren't using Django Models as entities we would be able to embed this object directly into the aggregate root.
    """
    EXPECTED_MAX_AMOUNT: ClassVar[Decimal] = Decimal("1000000")

    client_id: uuid.UUID
    submission_datetime: datetime
    amount: Decimal

    def __post_init__(self):
        self.validate_price()
        self.validate_client_id()

    def validate_price(self):
        if self.amount < 0:
            raise Exception("Prices must be positive")

    def validate_client_id(self):
        if uuid.UUID != type(self.client_id):
            raise Exception("The provided client id is not a UUID")

    def unexpected_amount_check(self) -> Tuple[TransactionWarning]:
        warning_list = []
        if self.price > self.EXPECTED_MAX_AMOUNT:
            w = TransactionWarning(1, "The provided price appears to be too high")
            warning_list.append(w)
        return tuple(warning_list)



class TransactionFactory():
    @staticmethod
    def build_entity_with_id(params: TransactionParams):
        id = uuid.uuid4()
        params_dict = asdict(params, skip_empty=True)
        transaction = Transaction(id=id, **params_dict)
        transaction.check_invariants()
        return transaction
