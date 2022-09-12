import csv
from urllib import response
from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
# from organisations.forms import UploadForm

from utils.exceptionhandler import CustomException
from .models import Csv, Organisation
from .serializers import CSVUploadSerializer, OrganisationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, render, get_object_or_404

# from inventorymanagementsystem.organisations import serializers

class OrganisationView(viewsets.ModelViewSet):
    """Organisation level view class for CRUD operations"""

    queryset = Organisation.objects.order_by("id")
    lookup_field = "organisation_uid"
    serializer_class = OrganisationSerializer
    # permission_classes = [IsAuthenticated]

    # def list(self,request, *args, **kwargs):
    #     print(request.meta.USERNAME)

    def destroy(self, request, *args, **kwargs):
        """destroy method overrided from ModelViewSet class for deleting
        Categories"""

        try:
            super().destroy(request)
            return Response({"message": "Organisation Deleted"})
        except Http404:
            raise CustomException(404, "Object not available")

    
class CSVUploadView(viewsets.ModelViewSet):
    """Export and Import CSV"""

    queryset = Csv.objects.all()
    serializer_class = CSVUploadSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'decrypt.html'

    def create(self, request, *args, **kwargs):
        # print(request.GET.get('File'))
        # csv_rev = reverse('csv-post')
        print(request.POST)
        print(request.FILES)
        # form = UploadForm(request.POST, request.FILES)
        # csv_upl = get_list_or_404(Csv)
        # serializer = CSVUploadSerializer(csv_upl, data=request.data)
        # if serializer.is_valid():
            # return Response({'serializer': serializer})
        # print("inside create")
        # serializer = CSVUploadSerializer()
        # context =CSVUploadSerializer(data=request.data)
        # return render(request,'decrypt.html',{})
        redirect('http://localhost:8000/organisation/')

    def list(self, request, *args, **kwargs):
        print("Inside List")    
        # file = request.FILES['file']
        # print(type(file))
        # print(request.reverse('upload'))
        # print(request.FILES['file'])
        # csvupload = get_list_or_404(Csv)
        # csv_rev = reverse('csv-list')
        serialize = CSVUploadSerializer()
        # if serializer.is_valid():
            # return Response({'serializer': serializer})
        # serializer.save()
        # return HttpResponseRedirect(csv_rev)
        # return render(request, 'decrypt.html', {'form' : form})
        return Response({'serializer' : serialize}, template_name = 'decrypt.html')
        # return render(request, "decrypt.html")

    def retrieve(self, request, *args, **kwargs):
        print("Sasikumar")
        serializer = CSVUploadSerializer()
        csv_upl = get_object_or_404(Csv)

        # return redirect(request.FILES,'decrypt.html')
        return Response({'serializer': serializer})

    # def upload_file(self, request):
    #     csvupload = get_object_or_404(csvupload)
    #     serializer = CSVUploadSerializer(csvupload, data=request.data)
    #     if not serializer.is_valid():
    #         return Response({'serializer': serializer})
    #     serializer.save()
    #     return redirect('decrypt')

# def upload(request):
#     print("Sasikumarrrrrrrrr")
#     form = UploadForm(request.POST, request.FILES)
#     print(request.FILES)
#     return render(request.FILES, 'decrypt.html', {'form' : form})
