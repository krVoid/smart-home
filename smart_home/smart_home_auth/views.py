import os

from django.http import HttpResponse
from rest_framework import generics, permissions
from django.contrib.auth.models import Group, User
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from oauth2_provider.models import RefreshToken, AccessToken
import requests
from collections import Counter
from oauth2_provider.models import RefreshToken
from . import serializers
from invitations.utils import get_invitation_model

BASE_URL = str(os.getenv("API_URL"))+'/auth/o/'

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")



class UserLoginRateThrottle(SimpleRateThrottle):
    scope = 'loginAttempts'

    def get_cache_key(self, request, view):
        user = User.objects.filter(username=request.data.get('username'))
        ident = user[0].pk if user else self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

    def allow_request(self, request, view):
        if self.rate is None:
            return True

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()

        if len(self.history) >= self.num_requests:
            return self.throttle_failure()

        if len(self.history) >= 3:
            data = Counter(self.history)
            for key, value in data.items():
                if value == 2:
                    return self.throttle_failure()
        return self.throttle_success(request)

    def throttle_success(self, request):
        user = User.objects.filter(username=request.data.get('username'))
        if user:
            self.history.insert(0, user[0].id)
        self.history.insert(0, self.now)
        self.cache.set(self.key, self.history, self.duration)
        return True

class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([UserLoginRateThrottle])
def token(request):
    try:
        r_username = request.data['username']
        r_password = request.data['password']
        user = User.objects.get(username=r_username)
        if user.check_password(r_password):
            r = requests.post(
                BASE_URL +'token/',
                data={
                    'grant_type': 'password',
                    'username': request.data['username'],
                    'password': request.data['password'],
                    'client_id': os.getenv("CLIENT_ID"),
                    'client_secret': os.getenv("CLIENT_SECRET"),
                },
            )
            return Response(r.json())
        else:
            return Response({'Password not match'}, status=400)
    except User.DoesNotExist:
        return Response({'Username not exist'}, status=400)



@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request): 
    r = requests.post(
        BASE_URL +'revoke_token/',
        data={
            'token': request.data['token'],
            'client_id': os.getenv("CLIENT_ID"),
            'client_secret': os.getenv("CLIENT_SECRET"),
        },
    )

    return Response(r, r.status_code)



@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    acces_token_id = AccessToken.objects.get(token=request.data['token']).id
    if acces_token_id:
        refresh_token = RefreshToken.objects.get(access_token=acces_token_id)
        if refresh_token: 
            r = requests.post(
                BASE_URL +'token/',
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                    'client_id': os.getenv("CLIENT_ID"),
                    'client_secret': os.getenv("CLIENT_SECRET"),
                },
            )
            return Response(r.json(), r.status_code)
        else:
            return Response({"Refresh Token not exist"}, status=400)
    return Response({"Token not exist"}, status=400)


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
                'email': request.data['email'],
                'client_id': os.getenv("CLIENT_ID"),
                'client_secret': os.getenv("CLIENT_SECRET"),
            },
        )
        return Response(r.json())
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def is_superuser(request):
    is_superuser = User.objects.get(username=request.user).is_superuser
    return Response(is_superuser)

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def send_invitation(request):
    Invitation = get_invitation_model()
    invite = Invitation.create('kingarojek13@gmail.com', inviter=request.user)
    invite.send_invitation(request)
