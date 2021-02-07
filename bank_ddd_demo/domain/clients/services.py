from .models import ClientFactory
from .models import Client

class ClientServices():

    @staticmethod
    def get_client_factory():
        return ClientFactory

    @staticmethod
    def get_client_repo():
        return Client.objects

