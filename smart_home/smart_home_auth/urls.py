from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('users/', views.UserList.as_view()),
    path('users/<pk>/', views.UserDetails.as_view()),
    path('groups/', views.GroupList.as_view()),
    path('token/', views.token), 
    path('revoke_token/', views.revoke_token),
    path('refresh_token/', views.refresh_token),
    path('register/', views.register),
    path('is_superuser/', views.is_superuser),
    path('send_invite/', views.send_invitation)
]


