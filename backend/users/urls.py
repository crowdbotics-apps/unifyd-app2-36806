from django.urls import path

from users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
    VerifyPasswordToken,
    ResendUserToken,
    VerifyUserToken,
    SendPasswordToken,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path('email/verify-user/',VerifyUserToken.as_view()),
    path('email/resend-token/',ResendUserToken.as_view()),
    path('reset-password/send/',SendPasswordToken.as_view()),
    path('reset-password/verify/',VerifyPasswordToken.as_view()),
]
