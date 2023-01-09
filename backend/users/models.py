from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from core.utils import get_file_path


class User(AbstractUser):
    # WARNING!
    """
    Some officially supported features of Crowdbotics Dashboard depend on the initial
    state of this User model (Such as the creation of superusers using the CLI
    or password reset in the dashboard). Changing, extending, or modifying this model
    may lead to unexpected bugs and or behaviors in the automated flows provided
    by Crowdbotics. Change it at your own risk.


    This model represents the User instance of the system, login system and
    everything that relates with an `User` is represented by this model.
    """

    # First Name and Last Name do not cover name patterns
    # around the globe.
    profile_image = models.ImageField(upload_to=get_file_path,null=True)
    friends = models.ManyToManyField('User', related_name='user_friends',blank=False)
    blocked = models.ManyToManyField('User', related_name='user_blocked',blank=False)
    followers = models.ManyToManyField('User',related_name='users_followers',blank=True)
    following = models.ManyToManyField('User',related_name='users_following',blank=True)
    is_private = models.BooleanField(default=False)
    zip_code = models.CharField(max_length=10,null=True)
    location = models.CharField(max_length=255,null=True)
    date_of_birth = models.DateField(null=True)
    longitude = models.FloatField(null=True,blank=True)
    latutude = models.FloatField(null=True,blank=True)


    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

class Preference(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    display_name_as = models.CharField(max_length=255)
    is_like_profile = models.BooleanField(default=True)
    is_hide_birthday = models.BooleanField(default=False)
    who_can_see_profile = models.CharField(max_length=255,default='Public')
    is_online_status = models.BooleanField(default=True)
    timezone = models.CharField(max_length=255,null=True)
    is_enable_chat = models.BooleanField(default=True)
    allow_new_message_friends = models.BooleanField(default=True)

class NotificationPreference(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    post_comment = models.BooleanField(default=True)
    post_reaction = models.BooleanField(default=True)
    comment_reaction = models.BooleanField(default=True)
    comment_reply = models.BooleanField(default=True)
    share_post = models.BooleanField(default=True)
    liked_my_profile = models.BooleanField(default=True)
    mention = models.BooleanField(default=True)
    new_message = models.BooleanField(default=True)
    friend_request = models.BooleanField(default=True)


class EmailTokenVerification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    token = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.user.email

class PasswordReset(EmailTokenVerification):
    pass


class ReportUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    reported_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reported_user')


class FriendRequests(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    sent_by = models.ForeignKey('User',on_delete=models.CASCADE,related_name='sent_by')
