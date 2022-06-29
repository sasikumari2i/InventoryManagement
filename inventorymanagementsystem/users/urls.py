from django.urls import path, include
from rest_framework import routers
from users import views

router = routers.DefaultRouter()
router.register("user", views.UserView)


urlpatterns = [path("user/login/", views.login_user),
               path("", include(router.urls))]

