"""inventorymanagementsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.http import HttpResponse, HttpResponseNotFound
# from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls
# from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    # TokenRefreshView,
# )
# import oauth2_provider
from utils.views import error_404, error_500
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# from oauth2_provider.models import AbstractApplication
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

# schema_view = get_swagger_view(title='Asset Management')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.assets.urls")),
    path("", include("apps.products.urls")),
    path("organisation/", include("organisations.urls")),
    path("", include("apps.orders.urls")),
    path("", include("apps.payments.urls")),
    path("api-auth/", include("rest_framework.urls")),
    # path('auth/', include('oauth2_provider.urls', namespace='oauth2_provider'))
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider'))
    # path('docs/', include_docs_urls(title='AssetManagement')),
    # path('schema', get_schema_view(
    #     title="Asset Management",
    #     description="Asset Management all APIs",
    #     version="1.0.0"
    # ), name='openapi-schema'),
    # path('swagger_schema', get_swagger_view(title='Asset Management')),

]

# ...

# schema_view = get_schema_view(
#    openapi.Info(
#       title="Snippets API",
#       default_version='v1'
#    ),
# )

# urlpatterns += [
#    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# ]


# urlpatterns += [
    # path("api-auth/", include("rest_framework.urls")),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
# ]

handler404 = error_404
handler500 = error_500

# urlpatterns += [
#    path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#    path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#    path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#    ...
# ]


