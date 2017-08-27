# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth.models import User


class UserRegistrationService(generics.CreateAPIView):
    serializer_class = RegistrationUserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        response = super(UserRegistrationService, self).post(request, *args, **kwargs)
        if 'password' in response.data:
            response.data.pop('password')
        return response


class ProfileService(APIView):
    serializer_class = RespUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        ser = RespUserSerializer(request.user)
        return Response(ser.data)

