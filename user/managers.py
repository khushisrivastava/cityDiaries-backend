from django.contrib.auth.base_user import BaseUserManager
import random


class UserManager(BaseUserManager):
    """ 
    Custom user model manager 
    """

    def _create_user(self, phone, password, **kwargs):
        """ 
        This function is called by the create_user and create_superuser function to create and save the users. 
        """
        if not phone:
            raise ValueError("User must have a phone")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(phone=phone, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_user(self, phone, password=None, **kwargs):
        """ Creates and saves user with provided phone number and other details """
        kwargs.setdefault('is_superuser', False)
        if not password or len(password) == 0:
            password = ''.join(random.choices('_b1JWPNtMP-5wqxteEXQuMzuIy2RXLED2HnuAO3qB1c'))
        return self._create_user(phone, password, **kwargs)

    def create_superuser(self, phone, password, **kwargs):
        """ Creates and saves superuser with the provided phone and password """
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)

        if not kwargs.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True")
        if not kwargs.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True")

        return self._create_user(phone, password, **kwargs)
