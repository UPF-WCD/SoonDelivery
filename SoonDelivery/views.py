from io import StringIO
from json import decoder, encoder
import jwt
import json
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import serializers, viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.utils.serializer_helpers import JSONBoundField
from .serializers import (
    TestSerializer, 
    CreateUserSerializer,
    UserSerializer,
    LoginUserSerializer,
    CheckListSerializer, 
    CheckSerializer)
from .models import Test, Check_list,User
from knox.models import AuthToken

from .token import accout_activation_token
from .text import message

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,force_text
from django.contrib.sites.models import Site

class TestView(viewsets.ModelViewSet):
    serializer_class = TestSerializer
    queryset = Test.objects.all()

class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        # print(type(request.body))
        # print(request.body)
        # bod = request.body.decode('utf8').replace("'", '"')
        # print(type(bod))
        # print(bod)
        # datas=json.loads(bod)
        # try:
        #     validate_email(datas["school_email"])
        #     if User.objects.filter(school_email=datas["school_email"]).exists():
        #         return JsonResponse({"message" : "EXIST_EMAIL"}, status=400)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            host = request.get_host()
            full_path = request.get_full_path()
            print(host+full_path)

            current_site = request.get_full_path_info()
            current_site = get_current_site(current_site)
            print(request.get_full_path_info())

            # domain = current_site.domain
            domain = 'localhost:8000'
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = accout_activation_token.make_token(user)
            message_data = message(domain, uidb64, token)

            mail_title = "이메일 인증을 완료해주세요"
            qd = request.data
            emails = qd['school_email']
            mail_to = emails
            email = EmailMessage(mail_title, message_data, to=[mail_to])
            email.send()

            return Response(
                {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data, 
                #여기서 값을 넘겨주려고 했으나 쉽지 않음
                "token": AuthToken.objects.create(user)[1],
                }
            )
        # except KeyError:
        #     return JsonResponse({"message" : "INVALID_KEY"}, status=200)
        # except TypeError:
        #     return JsonResponse({"message" : "INVALID_TYPE"}, status=400)
        # except ValidationError:
        #     return JsonResponse({"message" : "VALIDATION_ERROR"}, status=400)

class Activate(View):
    def get(self, request, uidb64, token):
        try:
            # uid = force_text(urlsafe_base64_decode(uidb64.encode('utf-8')))
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = uid)

            if accout_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                return HttpResponse(' 계정이 활성화되었습니다.',status=status.HTTP_200_OK)
            return redirect('http://google.com') 
        except ValidationError:
            return JsonResponse({"message":"TYPE_ERROR"}, status=400)
        except KeyError:
            return JsonResponse({"message":"INVALID_KEY"}, status=400)


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