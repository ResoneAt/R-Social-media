from django.db import models
from datetime import datetime


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
