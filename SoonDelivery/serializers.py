from rest_framework import serializers
from .models import Test, User,Check_list
from django.contrib.auth import authenticate
from .token import accout_activation_token
from .text import message
from django.core.validators import validate_email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,force_text

class TestSerializer(serializers.ModelSerializer):
  class Meta:
    model = Test
    fields = '__all__'

#회원가입
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "school_email","is_active")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if User.objects.filter(school_email = value).exists():
            raise serializers.ValidationError("이메일이 이미 존재합니다.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],  validated_data["password"], validated_data["school_email"],
            is_active=False
        )
        user.set_password(validated_data['password'])
        user.save()
        #여기서 현재 주소값을 넘겨줘야하는데 못 넘겨주고 있음
        # current_site = get_current_site(get_host)
        # domain = current_site.domain
        # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        # token = accout_activation_token.make_token(user)
        # message_data = message(domain, uidb64, token)

        # mail_title = "이메일 인증을 완료해주세요"
        # mail_to = validated_data["school_email"]
        # email = EmailMessage(mail_title, message_data, to=[mail_to])
        # email.send()

        return user

#접속 유지 중인가?
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


#로그인
class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")




class CheckListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Check_list
    fields = ['id', 'place', 'stuffList']

class CheckSerializer(serializers.ModelSerializer):
  class Meta:
    model = '__all__'