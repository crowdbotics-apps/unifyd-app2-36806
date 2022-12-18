from rest_framework import serializers
from posts.serializers import PostLikeSerializerGET
from groups import models


class GroupCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GroupCategory
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tags
        fields = '__all__'


class GroupSerializerGET(serializers.ModelSerializer):
    category = GroupCategorySerializer()
    tags = TagSerializer()

    class Meta:
        model = models.GroupCategory
        fields = '__all__'

class GroupSerializerGET(serializers.ModelSerializer):
    category = GroupCategorySerializer()
    tags = TagSerializer()

    class Meta:
        model = models.Group
        fields = '__all__'

class GroupSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        exclude = ('user',)


class GroupPostSerializerGET(serializers.ModelSerializer):
    group = GroupSerializerGET()
    post = PostLikeSerializerGET()

    class Meta:
        model = models.GroupPost
        fields = '__all__'

class GroupPostSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = models.GroupPost
        fields = '__all__'

