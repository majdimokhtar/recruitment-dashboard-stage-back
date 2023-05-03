from django.urls import path

from . import views

urlpatterns = [
    path("jobs/" , views.getAllJobs, name= "jobs"),
    path("jobs/addjob/" , views.addJob, name= "add-job"),
    path("jobs/<str:id>/" , views.getJob, name= "jobs" ),
    path("jobs/<str:id>/update/" , views.updateJob, name= "update-job" ),
    path("jobs/<str:id>/delete/" , views.deleteJob, name= "delete-job"),
    path("stats/<str:topic>/" , views.getTopicStats, name= "statics-jobs"),
    path("jobs/<str:id>/apply/" , views.applyToJob, name= "apply-jobs"),
    path("me/jobs/applied/" , views.getAppliedUser, name= "applied-user"),
    path("me/jobs/" , views.getCurrentUserJobs, name= "current-user-applied-jobs"),
    path("jobs/<str:id>/check/" , views.isApplied, name= "isapplied-to-job" ),
    path("job/<str:id>/candidates/" , views.getCandidatesApplied, name= "get-candidates-applied" ),
]
