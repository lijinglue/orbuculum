from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.core.validators import MinLengthValidator
from webapp.models import Account


class RespUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class RegistrationUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(validators=[MinLengthValidator(8)])

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password')
