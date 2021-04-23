from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    firebase_id = models.CharField(
        "Firebase ID", max_length=128, blank=False, unique=True)
    phone = models.CharField("Phone", max_length=17,
                             blank=False, unique=True)
    name = models.CharField("Name", max_length=255, blank=True)
    fav_places = models.ManyToManyField("core.Place")

    is_verified = models.BooleanField("Is Verified", default=False)
    is_staff = models.BooleanField("Is Staff", default=False)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.id)