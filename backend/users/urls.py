from django.urls import path,include
from rest_framework import routers
from users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
    VerifyPasswordToken,
    ResendUserToken,
    VerifyUserToken,
    SendPasswordToken,
    ProfileModelViewSet,
    FriendsModelViewSet,
    BlockedUserModelViewSet,FriendRequestModelViewSet,
    AcceptFriendRequest,
    BlockFriend,
    UnBlockFriend,
    GetFollowers,
    GetFollowing,
    ChangePassword
)
router = routers.DefaultRouter()
router.register('profile', ProfileModelViewSet,basename='profile')
router.register('friends', FriendsModelViewSet,basename='friend')
router.register('blocked', BlockedUserModelViewSet,basename='blocked')
router.register('friend-request', FriendRequestModelViewSet,basename='friend-request')

app_name = "users"
urlpatterns = [
    path('', include(router.urls)),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path('email/verify-user/',VerifyUserToken.as_view()),
    path('email/resend-token/',ResendUserToken.as_view()),
    path('reset-password/send/',SendPasswordToken.as_view()),
    path('reset-password/verify/',VerifyPasswordToken.as_view()),
    path('accept/friend-request/',AcceptFriendRequest.as_view()),
    path('block/user/',BlockFriend.as_view()),
    path('unblock/user/',UnBlockFriend.as_view()),
    path('follow/get-followers/',GetFollowers.as_view()),
    path('follow/get-following/',GetFollowing.as_view()),
    path('password/change/',ChangePassword.as_view()),
]
