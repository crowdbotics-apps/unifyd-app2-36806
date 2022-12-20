from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import filters
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from groups import models,serializers

class GroupCategoryModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return serializers.GroupCategorySerializer

    def get_queryset(self):
        return models.GroupCategory.objects.all()


class TagsModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return serializers.TagSerializer

    def get_queryset(self):
        return models.Tags.objects.all()


class GroupModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.GroupSerializerGET
        if self.action == 'retrieve':
            return serializers.GroupSerializerGET
        return serializers.GroupSerializerPOST

    def get_queryset(self):
        return models.Group.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AllGroupModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['name','category__name','tags__name']
    search_fields = ['name','category__name','tags__name']
    http_method_names = ['get']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.GroupSerializerGET
        if self.action == 'retrieve':
            return serializers.GroupSerializerGET
        return serializers.GroupSerializerPOST

    def get_queryset(self):
        return models.Group.objects.all()

class GroupPostModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.GroupPostSerializerGET
        if self.action == 'retrieve':
            return serializers.GroupPostSerializerGET
        return serializers.GroupPostSerializerPOST

    def get_queryset(self):
        return models.GroupPost.objects.filter(post__is_group_post=True,
            post__user = self.request.user)

class AllGroupPostModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.GroupPostSerializerGET
        if self.action == 'retrieve':
            return serializers.GroupPostSerializerGET
        return serializers.GroupPostSerializerPOST

    def get_queryset(self):
        return models.Group.objects.all()

# class ChangePassword(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self,request):
#         try:
#             category = models.GroupCategory.objects.annotate(total = )
#             return Response({"message":"Successfully Password changed."},status=status.HTTP_201_CREATED)
#         except Exception as e:
#              return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)