from django.db import models
from django.contrib.auth.models import User


class StoreOwner(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    email = models.EmailField(max_length=20, null=True, unique=True)

    def __str__(self):
        return self.name
