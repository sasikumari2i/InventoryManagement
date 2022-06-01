from django.urls import path, include
from rest_framework import routers

from organisations import views
from utils.views import error_404, error_500

router = routers.DefaultRouter()
router.register("organisations", views.OrganisationView)

urlpatterns = [path("", include(router.urls))]

handler404 = error_404
handler500 = error_500
