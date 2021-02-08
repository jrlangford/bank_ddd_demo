# python imports
import uuid
from typing import Tuple
from decimal import Decimal

# django imports
from django.db import transaction

# app imports
from bank_ddd_demo.domain.users.models import User, UserPersonalData, UserBasePermissions
from bank_ddd_demo.domain.users.services import UserServices

from bank_ddd_demo.domain.clients.models import Client, ClientPlatformUsageData
from bank_ddd_demo.domain.clients.services import ClientServices

from bank_ddd_demo.domain.transactions.models import Transaction, TransactionParams
from bank_ddd_demo.domain.transactions.services import TransactionServices

class UserAppServices():
    user_factory = UserServices.get_user_factory()

    @classmethod
    def create_user(cls, personal_data: UserPersonalData, base_permissions: UserBasePermissions) -> User:
        # This method is not strictly necessary since it only wraps a call to the user factory.
        user = cls.user_factory.build_entity_with_id(personal_data, base_permissions)
        # NOTE: This does not handle user password
        user.save()
        return user

class ClientAppServices():
    user_factory = UserServices.get_user_factory()
    client_repo = ClientServices.get_client_repo()
    client_factory = ClientServices.get_client_factory()

    @classmethod
    def create_system_client(cls, personal_data: UserPersonalData, base_permissions: UserBasePermissions) -> Tuple[User, Client]:
        # This method is in the application layer because it depends on both the users and clients modules
        # Since factories are in charge of id creation we do not hit the DB for entity creation
        user = cls.user_factory.build_entity_with_id(personal_data, base_permissions)
        client = cls.client_factory.build_entity(user.id, ClientPlatformUsageData())
        # We hit the DB only once, during save
        with transaction.atomic():
            user.save()
            client.save()
        return (user, client)

    @classmethod
    def get_client_from_user(cls, user: User) -> Client:
        # This method is in the application layer because it depends on both the users and clients modules
        # TODO: raise exception if user does not exist
        client = cls.client_repo.get(id=user.id)
        if client == None:
            raise Exception("Requested client does not exist")
        return client


class TransactionAppServices():
    transaction_factory = TransactionServices.get_transaction_factory()

    @classmethod
    def create_transaction(cls, user: User, params: TransactionParams) -> Transaction:
        # This method is in the application layer because it depends on both the users and transactions modules
        # TODO: run business logic on user, such as checking he has not transacted more money than he has on an account
        # Since the factory is in charge of id creation we do not hit the DB for entity creation
        t = cls.transaction_factory.build_entity_with_id(params)
        # We hit the DB only once, during save
        t.save()
        return t
