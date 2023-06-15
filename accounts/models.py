from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import MyUserManager


class User(AbstractBaseUser):
    username = models.CharField(max_length=73, unique=True)
    first_name = models.CharField(max_length=73, blank=True, null=True)
    last_name = models.CharField(max_length=73, blank=True, null=True )
    bio = models.TextField(max_length=730, blank=True, null=True)
    male = 1
    female = 2
    gender_choice = ((male, 'male'),(female, 'female'))
    gender = models.IntegerField(choices=gender_choice, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class RelationModel(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)
    allowed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'{self.from_user.username} follows {self.to_user.username}'


class ImageUserModel(models.Model):
    image = models.ImageField(upload_to='users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='image')
    alt = models.CharField(max_length=73)


class ReportUserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_reported = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_user')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_reported.username} - {self.body[:20]}...'


class MessageModel(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user.username} to {self.to_user.username} - {self.message[:20]}...'


class NotificationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=73)
    body = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} for user {self.user.username}'






