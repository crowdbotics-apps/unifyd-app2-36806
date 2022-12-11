
from rest_framework import serializers
from users import models

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('id','name','email','username','profile_image')

class ReportUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ReportUser
        exclude = ('added_by',)

class FriendRequestSerializerPOST(serializers.ModelSerializer):

    class Meta:
        model = models.FriendRequests
        exclude = ('sent_by',)

class FriendRequestSerializerGET(serializers.ModelSerializer):
    user = ProfileSerializer()
    sent_by = ProfileSerializer()

    class Meta:
        model = models.FriendRequests
        fields = '__all__'