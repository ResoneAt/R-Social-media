from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import MyUserManager
from core.models import BaseModel
from django.urls import reverse


class User(AbstractBaseUser):
    username = models.CharField(max_length=73, unique=True)
    first_name = models.CharField(max_length=73, blank=True, null=True)
    last_name = models.CharField(max_length=73, blank=True, null=True )
    bio = models.TextField(max_length=730, blank=True, null=True)

    male = 1
    female = 2
    gender_choice = ((male, 'male'),(female, 'female'))
    gender = models.IntegerField(choices=gender_choice, blank=True, null=True)

    account_type_choices = (('public', 'Public'), ('privet', 'Privet'))
    account_type = models.CharField(max_length=10, choices=account_type_choices, default='public')

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

    def get_follower_count(self):
        return self.follower.count()

    def get_following_count(self):
        return self.following.count()

    def is_following(self, user):
        return self.following.filter(to_user=user).exists()

    def is_followed_by(self, user):
        return self.follower.filter(from_user=user).exists()

    def follow(self, user):
        relation = RelationModel(from_user=self, to_user=user)
        relation.save()

    def unfollow(self, user):
        relation = RelationModel.objects.get(from_user=self, to_user=user)
        relation.delete()

    def follow_request(self, user):
        request = FollowRequestModel(from_user=self, to_user=user)
        request.save()

    def get_follower_list(self):
        return User.objects.filter(following__to_user=self)

    def get_following_list(self):
        return User.objects.filter(follower__from_user=self)

    def get_follow_request_list(self):
        return FollowRequestModel.objects.filter(to_user=self)

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()

    def profile_images(self):
        return ImageUserModel.objects.filter(user=self)

    def main_profile_image(self):
        return ImageUserModel.objects.filter(user=self).latest()

    def get_report_post_list(self):
        return ReportUserModel.objects.filter(user=self)

    def change_to_privet_user_account_type(self):
        if self.account_type == 'public':
            self.account_type = 'privet'

    def change_to_public_user_account_type(self):
        if self.account_type == 'privet':
            self.account_type = 'public'

    def get_absolute_url(self):
        kwargs = {
            'user_id': self.pk
        }
        return reverse('accounts:user_profile', kwargs=kwargs)


class RelationModel(BaseModel):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'{self.from_user.username} follows {self.to_user.username}'


class FollowRequestModel(BaseModel):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_receive')

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'{self.from_user.username} to {self.to_user.username} - {self.created_at}'


class ImageUserModel(models.Model):
    image = models.ImageField(upload_to='users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='image')
    alt = models.CharField(max_length=73)

    def __str__(self):
        return f'{self.alt} - user : {self.user.username}'


class ReportUserModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_reported = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_user')
    body = models.TextField()

    def __str__(self):
        return f'{self.user_reported.username} - {self.body[:20]}...'


class MessageModel(BaseModel):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField()

    def __str__(self):
        return f'{self.from_user.username} to {self.to_user.username} - {self.message[:20]}...'


class NotificationModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=73)
    body = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.title} for user {self.user.username}'
