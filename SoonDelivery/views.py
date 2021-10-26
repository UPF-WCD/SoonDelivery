from django.shortcuts import get_object_or_404, render
from rest_framework import serializers, viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import (
    TestSerializer, 
    CreateUserSerializer,
    UserSerializer,
    LoginUserSerializer,
    CheckListSerializer, 
    CheckSerializer)
from .models import Test, Check_list
from knox.models import AuthToken


class TestView(viewsets.ModelViewSet):
    serializer_class = TestSerializer
    queryset = Test.objects.all()

class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        if len(request.data["username"]) < 6 or len(request.data["password"]) < 4:
            body = {"message": "short field"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data, 
                "token": AuthToken.objects.create(user)[1],
            }
        )
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )

class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

        
def check_list(request):
    checks = Check_list.objects.all()
    serializer = CheckListSerializer(checks, many='True')
    return Response(serializer.data)

def check_detail(request, check_id):
    check = get_object_or_404(Check_list, pk=check_id)
    serializer = CheckSerializer(check)
    return Response(serializer.data)

def create_check(request):
    serializer = CheckSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)