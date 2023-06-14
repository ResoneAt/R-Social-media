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


class ImagePostModel(models.Model):
    image = models.ImageField(upload_to='posts')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    alt = models.CharField(max_length=73)


class ReportPostModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    post = models.ForeignKey(PostModel, on_delete=models.PROTECT)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
