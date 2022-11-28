import datetime
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from posts import serializers,models
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from filters.filters import RelatedOrderingFilter
from django.db.models import Count

class UserPostModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        return models.Post.objects.filter(user=self.request.user).order_by('-created')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, url_path="share", methods=["POST"])
    def share_post(self, request, pk):
        original_post = self.get_object()
        user = request.user
        if original_post.original_post:
            original_post = original_post.original_post
        post = models.Post.objects.create(
            user=user,
            original_post=original_post,
        )
        return Response('Successfully shared the post.', status=status.HTTP_201_CREATED)

class AllUserPostModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PostSerializer
    http_method_names = ['get']
    filter_backends = [RelatedOrderingFilter,filters.SearchFilter,DjangoFilterBackend]
    ordering_fields = '__all__'
    filterset_fields=['user__id',]
    search_fields = ['user__id',]


    def get_queryset(self):
        return models.Post.objects.all().order_by('-created')

class PostCommentModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PostCommentSerializer
    filter_backends = [RelatedOrderingFilter,filters.SearchFilter,DjangoFilterBackend]
    ordering_fields = '__all__'
    filterset_fields=['post__id',]
    search_fields = ['post__id',]

    def get_queryset(self):
        if self.request.method == 'GET':
            return models.PostComment.objects.all()
        return models.PostComment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostLikeModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [RelatedOrderingFilter,filters.SearchFilter,DjangoFilterBackend]
    ordering_fields = '__all__'
    filterset_fields=['post__id',]
    search_fields = ['post__id',]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PostLikeSerializerGET
        if self.action == 'retrieve':
            return serializers.PostLikeSerializerGET
        return serializers.PostLikeSerializerPOST

    def get_queryset(self):
        if self.request.method == 'GET':
            return models.PostLike.objects.all()
        return models.PostLike.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentLikeModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [RelatedOrderingFilter,filters.SearchFilter,DjangoFilterBackend]
    ordering_fields = '__all__'
    filterset_fields=['comment__id',]
    search_fields = ['comment__id',]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CommentLikeSerializerGET
        if self.action == 'retrieve':
            return serializers.CommentLikeSerializerGET
        return serializers.CommentLikeSerializerPOST

    def get_queryset(self):
        if self.request.method == 'GET':
            return models.CommentLike.objects.all()
        return models.CommentLike.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FlagPostModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.FlagPostSerializer
    http_method_names = ['post','delete']

    def get_queryset(self):
        return models.FlagPost.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class TrendingPostViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PostSerializer
    http_method_names = ['get']

    def get_queryset(self):
        now = datetime.datetime.now()
        week_start = now - datetime.timedelta(days=now.weekday())
        trends = list(models.PostLike.objects.filter(post__created__date=
        week_start.date()).values('post').annotate(total=Count('post')
        ).order_by('-total'))
        trends_ids = [trend['post'] for trend in trends]
        posts = models.Post.objects.in_bulk(trends_ids)
        sorted_posts = [posts[id] for id in trends_ids]
        return sorted_posts

