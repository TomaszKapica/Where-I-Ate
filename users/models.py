from django.db import models
from django.contrib.auth.models import AbstractUser


class RestaurantUser(AbstractUser):
    class Meta:
        permissions = (

        )


