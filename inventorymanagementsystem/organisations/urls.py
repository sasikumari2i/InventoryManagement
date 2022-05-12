from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from organisations import views

router = routers.DefaultRouter()
router.register('organisations', views.OrganisationView)

urlpatterns = [
    path('',include(router.urls))
]