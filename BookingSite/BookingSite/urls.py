"""BookingSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from conference_app.views import (
    AddRoomView,
    ListAllRoomsView,
    ModifyRoomView,
    ReserveRoomView,
    DeleteRoomView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^room/new/$', AddRoomView.as_view(), name='add-room'),
    re_path(r'^room/modify/(?P<id>\d+)/$', ModifyRoomView.as_view(), name='modify-room'),
    re_path(r'^room/reserve/(?P<id>\d+)/$', ReserveRoomView.as_view(), name='reserve-room'),
    re_path(r'^room/delete/(?P<id>\d+)/$', DeleteRoomView.as_view(), name='delete-room'),
    re_path(r'^rooms/$', ListAllRoomsView.as_view(), name='all-rooms'),
]
