from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class CategoryView(viewsets.ModelViewSet):
    """Gives the view for the Category"""

    queryset = Category.objects.get_queryset().order_by('id')
    serializer_class = CategorySerializer

class ProductView(viewsets.ModelViewSet):
    """Gives the view for the Product"""

    queryset = Product.objects.get_queryset().order_by('id')
    serializer_class = ProductSerializer
