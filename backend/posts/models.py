from users.views import User
from django.db import models
from core.utils import get_file_path
from django.contrib.postgres.fields import JSONField

class Post(models.Model):
    text = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    images = models.ImageField(upload_to=get_file_path,null=True,blank=True)
    created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customization = JSONField(null=True,blank=True)
    original_post = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True,
        related_name="post_original",
    )
    is_group_post = models.BooleanField(default=False)
    is_poll = models.BooleanField(default=False)
    is_multiple_poll = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.text + ' | ' + self.user.email

class PostComment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True,
        related_name="parent_comment",
    )
    date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.post.id) + ' | ' + self.user.email

class CommentLike(models.Model):
    comment = models.ForeignKey(PostComment,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)    

    def __str__(self) -> str:
        return str(self.comment.id) + ' | ' + self.user.email
class PostLike(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.post.id) + ' | ' + self.user.email

class FlagPost(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    reason = models.TextField()
    reason_type = models.CharField(max_length=255,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.post.id) + ' | ' + self.reason