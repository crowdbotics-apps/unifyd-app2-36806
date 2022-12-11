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
    name = models.CharField(_("Name of User"), blank=True, null=True, max_length=255)
    profile_image = models.ImageField(upload_to=get_file_path,null=True)
    friends = models.ManyToManyField('User', related_name='user_friends',blank=False)
    blocked = models.ManyToManyField('User', related_name='user_blocked',blank=False)
    is_private = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

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
