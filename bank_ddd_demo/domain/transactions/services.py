from .models import TransactionFactory
from .models import Transaction

class TransactionServices():

    @staticmethod
    def get_transaction_factory():
        return TransactionFactory

    @staticmethod
    def get_transaction_repo():
        return Transaction.objects

