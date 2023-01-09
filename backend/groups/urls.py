from django.urls import path,include
from rest_framework import routers
from groups import views

router = routers.DefaultRouter()
router.register('group-category', views.GroupCategoryModelViewSet,basename='group-category')
router.register('tags', views.TagsModelViewSet,basename='tags')
router.register('group', views.GroupModelViewSet,basename='group')
router.register('all-group', views.AllGroupModelViewSet,basename='all-group')
router.register('group-post', views.GroupPostModelViewSet,basename='all-group')
router.register('all-group-post', views.AllGroupPostModelViewSet,basename='all-group-post')

urlpatterns = [
    path('', include(router.urls)),
    path('group-category-count/',views.GetCategoryCount.as_view()),
    path('group-remove-member/',views.RemoveUserGroup.as_view())
]