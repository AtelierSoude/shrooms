

from actstream import action
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response

# from .models import *
# from .mixins import *
# from .forms import *
from .serializers import PermissionSerializer, UserSerializer


# Create your views here.


class RegisterUser(generics.CreateAPIView):
    """
    Register new user
    No permission restriction
    """
    queryset = get_user_model().objects.all()
    serializer_class=UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        target = self.perform_create(serializer)
        action.send(target, verb='s\'est inscrit')
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self,serializer):
        return serializer.save()

class UserViewSet(viewsets.ModelViewSet):
    """
    Liste et détail des utilisateurs
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        target = self.perform_create(serializer)
        action.send(request.user, verb='a inscrit', target=target)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self,serializer):
        return serializer.save()

class PermissionViewSet(viewsets.ModelViewSet):
    """
    Liste et détail des permissions
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
