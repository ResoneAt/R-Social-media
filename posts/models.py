from django.db import models
from accounts.models import User
# Create your models here.


class PostModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    slug = models.SlugField()
    location = models.CharField(max_length=730,blank=True, null=True)
    created_time = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.slug
