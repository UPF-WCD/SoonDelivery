from rest_framework import serializers
from .models import Test, User,Check_list
from django.contrib.auth import authenticate

class TestSerializer(serializers.ModelSerializer):
  class Meta:
    model = Test
    fields = '__all__'
#회원가입
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "school_email")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],  validated_data["password"], validated_data["school_email"]
        )
        user.set_password(validated_data['password'])
        user.save()
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