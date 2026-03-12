from django.contrib import admin
from django.urls import path
from portal import views

urlpatterns = [
    path('',views.home,name="home"),
]