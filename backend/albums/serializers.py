from dataclasses import fields
from tkinter import E
from rest_framework import serializers
from albums import models


class AlbumMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AlbumMedia
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
            try:
                images = models.AlbumMedia.objects.filter(album=obj)
                return AlbumMediaSerializer(images,many=True).data
            except Exception as e:
                print(e)
                return None
    class Meta:
        model = models.Album
        exclude = ('user', )

    def create(self,validated_data):
        album = super(AlbumSerializer, self).create(validated_data)
        try:
            images = dict(self.context.get('view').request.FILES)['image_objects']
        except Exception as e:
            print(e)
            images = []

        if images:
            for i in images:
                models.AlbumMedia.objects.create(
                    images = i,
                    album= album
                )
        return album