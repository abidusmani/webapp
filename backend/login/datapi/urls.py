# urls.py
from django.urls import path
from .views import UserListCreateView

urlpatterns = [
    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),
]
