
from rest_framework import serializers
from users import models

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('id','first_name','last_name',
        'email','username','zip_code',
        'location','date_of_birth',
        'profile_image')

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

class PreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Preference
        exclude = ('user',)

class NotificationPreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NotificationPreference
        exclude = ('user',)
