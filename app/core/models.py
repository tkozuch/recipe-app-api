from typing import Any
from django.db import models  # noqa
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must not be empty")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MyUserManager()

    USERNAME_FIELD = "email"


# class Artist(models.Model):
#     name = models.CharField(max_length=10)


# class Album(models.Model):
#     artist = models.ForeignKey(Artist, on_delete=models.CASCADE)


# class Song(models.Model):
#     artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
#     album = models.ForeignKey(Album, on_delete=models.RESTRICT)
