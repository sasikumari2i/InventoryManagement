# from django.urls import path, include
from unicodedata import name
from rest_framework import routers
from django.urls import path, include
from organisations import views
from utils.views import error_404, error_500

router = routers.DefaultRouter()
router.register("organisations", views.OrganisationView)
router.register("csvupload",views.CSVUploadView)

# app_name = 'organisations'

# urlpatterns = [
#     path("", include(router.urls)),
#     path('csv/upload', views.upload, name='upload')
# ]

# urlpatterns = [
#     path("csvupload/",views.CSVUploadView.as_view(), name='csv')
#     ]

urlpatterns = router.urls

handler404 = error_404
handler500 = error_500
