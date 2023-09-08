from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.BigIntegerField()
    role = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'password','phone_number',]
    
















# from django.db import models

# class User(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     email = models.CharField(unique=True, max_length=70)
#     password = models.CharField(max_length=45)
#     phone_number = models.BigIntegerField()
#     role = models.CharField(max_length=45)
#     status = models.CharField(max_length=45)
    