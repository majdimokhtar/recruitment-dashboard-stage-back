import requests
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import SignUpSerializer, UserSerializers
from .validators import validate_file_extension

# Get user from port 800.

def get_user_from_api(request):
    try:
        user_resp = requests.get(
            "http://127.0.0.1:8000/api/auth/user",
            headers={"Authorization": f"Bearer {request.auth}"},
        )
        user_resp.raise_for_status() # raise an exception if response status code is >= 400
    except requests.exceptions.RequestException as e:
        # handle request error, e.g. log the error or return None
        print(f"Error making API request: {e}")
        return None
    
    user_data = user_resp.json()
    user_dict = user_data.get("user")
    if user_dict is None:
        # handle the case where the "user" key is missing
        return None
    username = user_dict.get("email", "")
    users = User.objects.filter(username=username)
    if not users.exists():
        return None
    return users.first()



# Create your views here.

@api_view(["POST"])
def register(request):
    data = request.data

    user = SignUpSerializer(data=data)

    if user.is_valid():
        if not User.objects.filter(username=data["email"]).exists():
            user = User.objects.create(
                first_name=data["first_name"],
                last_name=data["last_name"],
                username=data["email"],
                email=data["email"],
                password=make_password(data["password"]),
            )

            return Response({"message": "User registered."}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

    else:
        return Response(user.errors)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def currentUser(request):
    user = get_user_from_api(request)
    if user:
        user_serializer = UserSerializers(user)
        return Response(user_serializer.data)
    else:
        return Response({"error": "Unable to retrieve user data"})


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateUser(request):
    user = request.user

    data = request.data
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.username = data["username"]
    user.email = data["email"]

    if data["password"] != "":
        user.password = make_password(data["password"])

    user.save()

    serializer = UserSerializers(user, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def uploadResume(request):
    user = get_user_from_api(request)
    if not user:
        return Response(
            {"error": "Failed to retrieve user"}, status=status.HTTP_400_BAD_REQUEST
        )
    # user = request.user
    resume = request.FILES.get("resume", None)

    if not resume:
        return Response(
            {"error": "Please upload your resume."}, status=status.HTTP_400_BAD_REQUEST
        )

    if resume.size > 2 * 1024 * 1024:
        return Response(
            {"error": "Please upload a resume that is 2 MB or smaller."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        isValidFile = validate_file_extension(resume.name)
    except ValidationError:
        return Response(
            {"error": "Please upload only PDF files."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not isValidFile:
        return Response(
            {"error": "Please upload only PDF files."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = UserSerializers(user, many=False)

    user.userprofile.resume = resume
    user.userprofile.save()

    return Response(serializer.data)





# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def currentUser(request):
#     user = get_user_from_api(request)
#     if not user:
#         return Response(
#             {"error": "Failed to retrieve user"}, status=status.HTTP_400_BAD_REQUEST
#         )
#     user = UserSerializers(request.user)


#     return Response(user.data)



# Get user from port 800.

# def get_user_from_api(request):
#     user_resp = requests.get(
#         "http://127.0.0.1:8000/api/auth/user",
#         headers={"Authorization": f"Bearer {request.auth}"},
#     )
#     if user_resp.status_code != 200:
#         return None
#     user_data = user_resp.json()
#     user_dict = user_data.get("user")
#     username = user_dict.get("email", "")
#     users = User.objects.filter(username=username)
#     if not users.exists():
#         return None
#     return users.first()




# def get_user_from_api(request):
#     user_resp = requests.get(
#         "http://127.0.0.1:8000/api/auth/user",
#         headers={"Authorization": f"Bearer {request.auth}"},
#     )
#     if user_resp.status_code != 200:
#         return None
#     user_data = user_resp.json()
#     user_dict = user_data.get("user")
#     if user_dict is None:
#         # handle the case where the "user" key is missing
#         return None
#     username = user_dict.get("email", "")
#     users = User.objects.filter(username=username)
#     if not users.exists():
#         return None
#     return users.first()