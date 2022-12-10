from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from core.utils import send_custom_email
from .models import PasswordReset,EmailTokenVerification
from core.utils import generateOTP
from users import serializers,models


User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class SendPasswordToken(APIView):
    def post(self,request):
        try:
            email = request.data['email']
            password_reset = PasswordReset.objects.filter(user__email=email)
            if password_reset.exists():
                    password_reset=password_reset.first()
                    send_custom_email(
                    "Password Reset Token",
                    f"Your Token for Password reset is {password_reset.token}",
                    password_reset.user.email)
                    return Response({"message":"Successfully Token sent."},status=status.HTTP_201_CREATED)
            token = generateOTP()
            user= User.objects.filter(email=email)
            if user.exists():
                user = user.first()
                PasswordReset.objects.create(
                    user = user,
                    token =token 
                )
                send_custom_email(
                    "Password Reset Token",
                    f"Your Token for Password reset is {token}",
                    user.email)
                return Response({"message":"Successfully Token sent."},status=status.HTTP_201_CREATED)
            return Response({"message":"User not found."},status=status.HTTP_201_CREATED)
            
        except Exception as e:
             return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

class VerifyPasswordToken(APIView):
    def post(self,request):
        try:
            email = request.data['email']
            token = request.data['token']
            user_verify = PasswordReset.objects.filter(user__email = email)
            if user_verify.exists():
                user_verify = user_verify.first()
                if token == user_verify.token:
                    user = user_verify.user
                    user.set_password(request.data['password'])
                    user.save()
                    user_verify.delete()
                    return Response({"message":"Successfully resetted user password."},status=status.HTTP_201_CREATED)
            return Response({"message":"Wrong Token."},status=status.HTTP_201_CREATED)
            
        except Exception as e:
             return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserToken(APIView):
    def post(self,request):
        try:
            email = request.data['email']
            token = request.data['token']
            user_verify = EmailTokenVerification.objects.filter(user__email = email)
            if user_verify.exists():
                user_verify = user_verify.first()
                if token == user_verify.token:
                    user = user_verify.user
                    user.is_active = True
                    user.save()
                    user_verify.delete()
                    token, created = Token.objects.get_or_create(user=user)
                    data = {}
                    data['message'] = "Successfully User activated"
                    data['token'] = token.key
                    return Response(data,status=status.HTTP_201_CREATED)
            return Response({"message":"Wrong Token."},status=status.HTTP_201_CREATED)
            
        except Exception as e:
             return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

class ResendUserToken(APIView):
    def post(self,request):
        try:
            email = request.data['email']
            user_verify = EmailTokenVerification.objects.filter(user__email = email)
            if user_verify.exists():
                user_verify = user_verify.first()
                send_custom_email(
                    "Email Verification Token",
                    f"Your Token for Email Verification is {user_verify.token}",
                    user_verify.user.email)
                return Response({"message":"Successfully resend Token"},status=status.HTTP_201_CREATED)
            return Response({"message":"User Doesn't exist"},status=status.HTTP_201_CREATED)
            
        except Exception as e:
             return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)



class ProfileModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['put','get']
    serializer_class = serializers.ProfileSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['email','username','name']
    search_fields = ['email','username','name']

    def get_queryset(self):
        if self.request.method == 'put':
            return User.objects.filter(id=self.request.user.id)
        return User.objects.all()
        

class FriendsModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    serializer_class = serializers.ProfileSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['email','username','name']
    search_fields = ['email','username','name']

    def get_queryset(self):
        return self.request.user.friends.all()

class BlockedUserModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    serializer_class = serializers.ProfileSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['email','username','name']
    search_fields = ['email','username','name']

    def get_queryset(self):
        return self.request.user.blocked.all()

class ReportUserModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']
    serializer_class = serializers.ReportUserSerializer

    def get_queryset(self):
        return models.ReportUser.objects.all()

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)


class AcceptFriendRequest(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            friend_request = models.FriendRequests.objects.get(id=request.data['fr_id'],user=request.user)
            friend_request.user.friends.add(friend_request.sent_by)
            friend_request.sent_by.friends.add(friend_request.user)
            friend_request.delete()
            return Response({"message":"Successfully Friend Request Accepted."},status=status.HTTP_201_CREATED)
            
        except Exception as e:
             return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

class BlockFriend(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            user = request.user
            block_user = User.objects.get(id=request.data['b_id'])
            user.friends.remove(block_user)
            user.blocked.add(block_user)
            user.save()
            return Response({"message":"Successfully Blocked User."},status=status.HTTP_201_CREATED)
            
        except Exception as e:
             return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

class UnBlockFriend(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            user = request.user
            block_user = User.objects.get(id=request.data['b_id'])
            user.blocked.remove(block_user)
            return Response({"message":"Successfully UnBlocked User."},status=status.HTTP_201_CREATED)
            
        except Exception as e:
             return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

class FriendRequestModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['post','get','delete']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.FriendRequestSerializerGET
        if self.action == 'retrieve':
            return serializers.FriendRequestSerializerGET
        return serializers.FriendRequestSerializerPOST

    def get_queryset(self):
        return models.FriendRequests.objects.filter(Q(user=self.request.user)
         | Q(sent_by=self.request.user))

    def perform_create(self, serializer):
        serializer.save(sent_by=self.request.user)

