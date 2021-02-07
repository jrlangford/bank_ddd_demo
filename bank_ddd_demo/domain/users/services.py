from .models import UserFactory
from .models import User

class UserServices():

    @staticmethod
    def get_user_factory():
        return UserFactory

    @staticmethod
    def get_user_repo():
        return User.objects
