# from django.conf import settings
# from rest_framework.response import Response
#
# class CustomMiddleware:
#
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         response = self.get_response(request)
#         return response
#
#     def process_view(self, request, view_func, view_args, view_kwargs):
#         response = view_func(request)
#         print(response)
