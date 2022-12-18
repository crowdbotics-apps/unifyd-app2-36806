from django.db import models
from core.utils import get_file_path
from posts.models import Post
from users.views import User

GROUP_CHOICES = (
    ('Open','Open'),
    ('Close','Close')
)

class GroupCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Tags(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(GroupCategory,on_delete=models.CASCADE)
    description = models.TextField(null=True)
    picture = models.ImageField(upload_to=get_file_path)
    tags = models.ManyToManyField(Tags,null=True)
    date = models.DateTimeField(auto_now_add=True)
    group_privacy = models.CharField(max_length=255,choices=GROUP_CHOICES,default='Open')
    members = models.ManyToManyField(User,null=True,related_name='group_members')
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class GroupPost(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
