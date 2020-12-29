from django.http import HttpResponse
from rest_framework import generics, permissions
from django.contrib.auth.models import User, Group
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User, Group
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import requests
from . import serializers
from smart_home.settings import CLIENT_ID, CLIENT_SECRET

BASE_URL = 'http://localhost:8000/auth/o/'

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    r = requests.post(
        BASE_URL +'token/',
        data={
            'grant_type': 'password',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    r = requests.post(
        BASE_URL +'revoke_token/',
        data={
            'token': request.data['token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )

    return Response(r, r.status_code)



@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    r = requests.post(
    BASE_URL +'token/', 
        data={
            'grant_type': 'refresh_token',
            'refresh_token': request.data['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = serializers.CreateUserSerializer(data=request.data) 
    if serializer.is_valid():
        serializer.save() 
        r = requests.post(BASE_URL +'token/', 
            data={
                'grant_type': 'password',
                'username': request.data['username'],
                'password': request.data['password'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )
        return Response(r.json())
    return Response(serializer.errors)