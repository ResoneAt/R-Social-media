from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import MyUserManager
from core.models import BaseModel
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models.manager import Manager


class User(AbstractBaseUser):
    username = models.CharField(max_length=73, unique=True, help_text='Please enter your username')
    first_name = models.CharField(max_length=73, blank=True, null=True, help_text='Please enter your first name')
    last_name = models.CharField(max_length=73, blank=True, null=True, help_text='Please enter your last name')
    bio = models.TextField(max_length=730, blank=True, null=True, help_text='Please write about yourself')

    male = 1
    female = 2
    gender_choice = ((male, 'male'),(female, 'female'))
    gender = models.IntegerField(choices=gender_choice, blank=True, null=True)
    image = models.ImageField(upload_to='users', null=True, blank=True, help_text='Please upload your image.')

    account_type_choices = (('public', 'Public'), ('privet', 'Privet'))
    account_type = models.CharField(max_length=10, choices=account_type_choices, default='public')

    phone_number = models.CharField(max_length=11, blank=True, null=True, help_text='Please enter your phone number.'
                                                                                    'A valid phone number must contain'
                                                                                    ' 11 digits.')
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        help_text='Please enter your email.( example@mail.com )'
    )
    date_of_birth = models.DateField(blank=True, null=True, help_text='example : 2010-07-23')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    deleted_at = models.DateField(blank=True, null=True, editable=False)
    is_deleted = models.BooleanField(blank=True, null=True, default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name, verbose_name_plural = _("User"), _("Users")

    def __str__(self):
        return self.email

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

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
        return self.following.count()

    def get_following_count(self):
        return self.follower.count()

    def get_request_count(self):
        return self.request_receive.count()

    def is_following(self, user_id):
        user = User.objects.get(pk=user_id)
        return self.follower.filter(to_user=user).exists()

    def is_follow_requesting(self, user_id):
        user = User.objects.get(pk=user_id)
        return self.request_sent.filter(to_user=user).exists()

    def is_followed_by(self, user_id):
        user = User.objects.get(pk=user_id)
        return self.following.filter(from_user=user).exists()

    def follow(self, user_id):
        user = User.objects.get(pk=user_id)
        relation = RelationModel(from_user=self, to_user=user)
        relation.save()

    def unfollow(self, user_id):
        user = User.objects.get(pk=user_id)
        relation = RelationModel.objects.get(from_user=self, to_user=user)
        relation.delete()

    def follow_request(self, user_id):
        user = User.objects.get(pk=user_id)
        request = FollowRequestModel(from_user=self, to_user=user)
        request.save()

    def accept_follow_request(self, user_id):
        user = User.objects.get(pk=user_id)
        request = FollowRequestModel.objects.get(from_user=user, to_user=self)
        request.delete()
        User.follow(user, self.pk)

    def reject_follow_request(self, user_id):
        user = User.objects.get(pk=user_id)
        request = FollowRequestModel.objects.get(from_user=user, to_user=self)
        request.delete()


    @staticmethod
    def is_privet(user_id):
        user = User.objects.get(pk=user_id)
        return user.account_type == 'privet'


    @staticmethod
    def get_follower_list(user_id):
        user = User.objects.get(pk=user_id)
        return User.objects.filter(follower__to_user=user)

    @staticmethod
    def get_following_list(user_id):
        user = User.objects.get(pk=user_id)
        return User.objects.filter(following__from_user=user)

    def get_requests_list(self):
        return FollowRequestModel.objects.filter(to_user=self)

    def get_follow_request_list(self):
        return FollowRequestModel.objects.filter(to_user=self)

    # def profile_images(self):
    #     return ImageUserModel.objects.filter(user=self)

    # def main_profile_image(self):
    #     return ImageUserModel.objects.filter(user=self).latest()

    def get_report_user_list(self):
        return ReportUserModel.objects.filter(user=self)

    def change_to_privet_user_account_type(self):
        if self.account_type == 'public':
            self.account_type = 'privet'

    def change_to_public_user_account_type(self):
        if self.account_type == 'privet':
            self.account_type = 'public'

    def new_message_count2(self, sender_id):
        sender = get_object_or_404(User, pk=sender_id)
        new_messages = MessageModel.objects.filter(is_read=False, from_user=sender, to_user=self)
        return new_messages.count()

    def all_of_new_messages_count(self):
        new_messages = MessageModel.objects.filter(is_read=False, to_user=self)
        return new_messages.count()

    def get_posts(self):
        return self.posts.all()

    def get_posts_count(self):
        return self.posts.count()

    def get_absolute_url(self):
        kwargs = {
            'user_id': self.pk
        }
        return reverse('accounts:user_profile', kwargs=kwargs)


class RecycleUser(User):

    deleted = Manager()
    class Meta:
        proxy = True


class RelationModel(BaseModel):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        unique_together = ('from_user', 'to_user')
        verbose_name, verbose_name_plural = _("Relation"), _("Relations")

    def __str__(self):
        return f'{self.from_user.username} follows {self.to_user.username}'


class FollowRequestModel(BaseModel):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_receive')

    class Meta:
        unique_together = ('from_user', 'to_user')
        verbose_name, verbose_name_plural = _("Follow Request"), _("Follow Requests")

    def __str__(self):
        return f'{self.from_user.username} to {self.to_user.username} - {self.created_at}'


# class ImageUserModel(BaseModel):
#     image = models.ImageField(upload_to='users', help_text='Please upload your image.')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='image')
#     alt = models.CharField(max_length=73, help_text='please write alt for image.')
#
#     class Meta:
#         verbose_name, verbose_name_plural = _("User Image"), _("User Images")
#
#     def __str__(self):
#         return f'{self.alt} - user : {self.user.username}'


class ReportUserModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter')
    user_reported = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_user')
    body = models.TextField(verbose_name=_('Report text'),
                            help_text='Please write the reason for reporting this user')

    class Meta:
        verbose_name, verbose_name_plural = _("Logged reports for user"), _("Logged reports for users")

    def __str__(self):
        return f'{self.user_reported.username} - {self.body[:20]}...'


class MessageModel(BaseModel):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField(help_text='Please write write your message')
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name, verbose_name_plural = _("Message"), _("Messages")

    def __str__(self):
        return f'{self.from_user.username} to {self.to_user.username} - {self.message[:20]}...'

    @staticmethod
    def seen_message(from_user_id, to_user_id):
        from_user = get_object_or_404(User, pk=from_user_id)
        to_user = get_object_or_404(User, pk=to_user_id)
        messages = MessageModel.objects.filter(is_read=False,
                                               from_user=from_user,
                                               to_user=to_user)
        messages.update(is_read=True)


class NotificationModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=73)
    body = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name, verbose_name_plural = _("Notification"), _("Notifications")

    def __str__(self):
        return f'{self.title} for user {self.user.username}'
