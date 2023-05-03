from rest_framework import serializers

from .models import CandidatesApplied, Job


class JobSerializers(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"


class CandidateAppliedSerializers(serializers.ModelSerializer):
    job = JobSerializers()

    class Meta:
        model = CandidatesApplied
        fields = ("user", "resume", "apliedAt", "job")
