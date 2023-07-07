from django.contrib.auth.models import BaseUserManager
from django.db.models import QuerySet
from django.utils import timezone


class CustomPostModelQueryset(QuerySet):
    def delete(self):
        return self.update(is_deleted=True, is_active=False, deleted_at=timezone.now())


class MyPostModelManager(BaseUserManager):

    def get_queryset(self):
        return CustomPostModelQueryset(self.model, self._db).filter(is_active=True, is_deleted=False)
