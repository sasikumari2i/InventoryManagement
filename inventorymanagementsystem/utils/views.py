from django.http import JsonResponse


def error_404(request, exception):

    message = "The requested page is not found"
    response = JsonResponse(data={"message": message, "status_code": 404})

    return response

def error_500(request):

    message = "Internal Server Error"
    response = JsonResponse(data={"message": message, "status_code": 500})

    return response

