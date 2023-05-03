from django.urls import path

from . import views

urlpatterns = [
    path("auth/register/" , views.register, name= "register"),
    path("me/" , views.currentUser, name= "current-user"),
    path("me/update/" , views.updateUser, name= "update-user"),
    path("upload/resume/" , views.uploadResume, name= "upload-resume"),
]
