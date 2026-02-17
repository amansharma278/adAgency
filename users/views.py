from django.http import JsonResponse
from django.shortcuts import render

from users.models import User
from users.serializer import UserSerializer


# Create your views here.
def signup(request):

    email = request.POST['email']
    password = request.POST['password']
    if email:
        return JsonResponse({
            "message":"Please enter your email address",
            "success":False,
        })
    user = User.objects.filter(email=email)
    if user:
        User.objects.create_user(email,password)
        return JsonResponse({
            "message": "Successfully created user",
            "success":True,
        })
    else:
        return JsonResponse({
            "message": "Something went wrong",
        })

def profile(request):
    user = request.user
    return JsonResponse({
        "user":UserSerializer(user).data,
    })


