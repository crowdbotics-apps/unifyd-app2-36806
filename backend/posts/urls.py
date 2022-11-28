from django.urls import path,include
from rest_framework import routers
from posts import views

router = routers.DefaultRouter()
router.register('all-posts', views.AllUserPostModelViewSet,basename='all-posts')
router.register('user-posts', views.UserPostModelViewSet,basename='user-post')
router.register('comments', views.PostCommentModelViewSet,basename='comment')
router.register('like', views.PostLikeModelViewSet,basename='like')
router.register('comment-like', views.CommentLikeModelViewSet,basename='comment-like')
router.register('flag-post', views.FlagPostModelViewSet,basename='flag-post')
router.register('trending-post', views.TrendingPostViewSet,basename='trending-post')

urlpatterns = [
    path('', include(router.urls)),
]