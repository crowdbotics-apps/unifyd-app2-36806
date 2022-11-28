from rest_framework import serializers
from notification import models

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        exclude = ('user',)