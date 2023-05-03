import requests
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg, Count, Max, Min
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import JobsFilter
from .models import CandidatesApplied, Job
from .serializers import CandidateAppliedSerializers, JobSerializers

# Get user from port 8000.

def get_user_from_api(request):
    try:
        user_resp = requests.get(
            "http://127.0.0.1:8000/api/auth/user",
            headers={"Authorization": f"Bearer {request.auth}"},
        )
        user_resp.raise_for_status()  # raise an exception if response status code is >= 400
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


@api_view(["GET"])
def getAllJobs(request):
    filterset = JobsFilter(
        request.GET, queryset=Job.objects.all().order_by("-createdAt")
    )
    count = filterset.qs.count()

    # pagination
    responsePerPage = 3
    paginator = Paginator(filterset.qs, responsePerPage)
    page_number = request.GET.get("page")
    try:
        queryset = paginator.page(page_number)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    serializer = JobSerializers(queryset, many=True)

    return Response(
        {"count": count, "responsePerPage": responsePerPage, "jobs": serializer.data}
    )


@api_view(["GET"])
def getJob(request, id):
    job = get_object_or_404(Job, id=id)
    candidates = job.candidatesapplied_set.all().count()
    serializer = JobSerializers(job, many=False)
    return Response({"job": serializer.data, "candidates": candidates})


# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def addJob(request):
#     request.data["user"] = request.user
#     data = request.data
#     job = Job.objects.create(**data)
#     serializer = JobSerializers(job, many=False)
#     return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addJob(request):
    user = get_user_from_api(request)
    if not user:
        return Response(
            {"error": "Failed to retrieve user"}, status=status.HTTP_400_BAD_REQUEST
        )

    request.data["user"] = user
    print(user)
    data = request.data
    job = Job.objects.create(**data)
    serializer = JobSerializers(job, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateJob(request, id):
    user = get_user_from_api(request)
    if not user:
        return Response(
            {"error": "Failed to retrieve user"}, status=status.HTTP_400_BAD_REQUEST
        )
    job = get_object_or_404(Job, id=id)
    if job.user != user:
        return Response(
            {"message": "you cannot update this job"}, status=status.HTTP_403_FORBIDDEN
        )

    job.title = request.data["title"]
    job.description = request.data["description"]
    job.email = request.data["email"]
    job.address = request.data["address"]
    job.jobType = request.data["jobType"]
    job.education = request.data["education"]
    job.industry = request.data["industry"]
    job.experience = request.data["experience"]
    job.salary = request.data["salary"]
    job.positions = request.data["positions"]
    job.company = request.data["company"]

    job.save()

    serializer = JobSerializers(job, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteJob(request, id):
    user = get_user_from_api(request)
    if not user:
        return Response(
            {"error": "Failed to retrieve user"}, status=status.HTTP_400_BAD_REQUEST
        )
    job = get_object_or_404(Job, id=id)
    if job.user != user:
        return Response(
            {"message": "you cannot delete this job"}, status=status.HTTP_403_FORBIDDEN
        )
    job.delete()
    return Response({"message": "job deleted!"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def getTopicStats(request, topic):
    args = {"title__icontains": topic}
    jobs = Job.objects.filter(**args)

    if len(jobs) == 0:
        return Response(
            {"message": "No Stats found for the {topic}".format(topic=topic)}
        )

    stats = jobs.aggregate(
        total_jobs=Count("title"),
        avg_positions=Avg("positions"),
        avg_salary=Avg("salary"),
        min_salary=Min("salary"),
        max_salary=Max("salary"),
    )
    return Response(stats)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def applyToJob(request, id):
    user = get_user_from_api(request)
    if not user:
        return Response(
            {"error": "Failed to retrieve user"}, status=status.HTTP_400_BAD_REQUEST
        )
    job = get_object_or_404(Job, id=id)

    if user.userprofile.resume == "":
        return Response(
            {"error": "please upload your resume first"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if job.lastDate < timezone.now():
        return Response(
            {"error": "You cannot apply to this job date is over"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    alreadyApplied = job.candidatesapplied_set.filter(user=user).exists()

    if alreadyApplied:
        return Response(
            {"error": "You already applied to this job"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    jobApplied = CandidatesApplied.objects.create(
        job=job, user=user, resume=user.userprofile.resume
    )
    return Response(
        {"applied": True, "job_id": jobApplied.id}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getAppliedUser(request):
    user = get_user_from_api(request)
    if not user:
        return Response(
            {"error": "Failed to retrieve user"}, status=status.HTTP_400_BAD_REQUEST
        )
    args = {"user": user}
    # args = {"user_id": request.user.id}
    jobs = CandidatesApplied.objects.filter(**args)

    serializer = CandidateAppliedSerializers(jobs, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def isApplied(request, id):
    user = get_user_from_api(request)
    if not user:
        return Response(
            {"error": "Failed to retrieve user"}, status=status.HTTP_400_BAD_REQUEST
        )
    # user = request.user
    job = get_object_or_404(Job, id=id)
    applied = job.candidatesapplied_set.filter(user=user).exists()
    return Response(applied)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCurrentUserJobs(request):
    user = get_user_from_api(request)
    if not user:
        return Response(
            {"error": "Failed to retrieve user"}, status=status.HTTP_400_BAD_REQUEST
        )

    args = {"user": user}

    jobs = Job.objects.filter(**args)
    serializer = JobSerializers(jobs, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCandidatesApplied(request, id):
    user = get_user_from_api(request)
    if not user:
        return Response(
            {"error": "Failed to retrieve user"}, status=status.HTTP_400_BAD_REQUEST
        )
    # user = request.user
    job = get_object_or_404(Job, id=id)

    if job.user != user:
        return Response(
            {"error": "you cannot access to this job"}, status=status.HTTP_403_FORBIDDEN
        )

    candidates = job.candidatesapplied_set.all()

    serializer = CandidateAppliedSerializers(candidates, many=True)

    return Response(serializer.data)
