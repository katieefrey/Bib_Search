from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
import hashlib
import time

#from search.models import Bibgroup

class Bibgroup(models.Model):
    bibgroup = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.bibgroup}"

class CustomUser(AbstractUser):
    # add additional fields in here
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    devkey = models.CharField(max_length=50, null=True, blank=True)
    bibgroup = models.ForeignKey(Bibgroup, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.username} {self.email}"
