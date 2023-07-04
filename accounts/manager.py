from django.contrib.auth.models import BaseUserManager
from django.db.models import QuerySet
from django.utils import timezone


class CustomUserQueryset(QuerySet):
    def delete(self):
        return self.update(is_deleted=True, is_active=False, deleted_at=timezone.now())


class MyUserManager(BaseUserManager):

    def get_queryset(self):
        return CustomUserQueryset(self.model, self._db).filter(is_active=True, is_deleted=False)

    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
