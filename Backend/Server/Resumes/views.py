from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from rest_framework.generics import get_object_or_404

from .models import JobSeekerResume, Experience, Education, JobSeekerSkill
from .serializers import (
    JobSeekerResumeSerializer,
    ExperienceSerializer,
    EducationSerializer,
    JobSeekerSkillSerializer,
)



# JobSeekerResume ViewSet
class JobSeekerResumeViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing JobSeekerResume model operations with custom permission.
    """
    queryset = JobSeekerResume.objects.all()
    serializer_class = JobSeekerResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


# Experience ViewSet
class ExperienceViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing Experience model operations with custom permission.
    """
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


# Education ViewSet
class EducationViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing Education model operations with custom permission.
    """
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


# JobSeekerSkill ViewSet
class JobSeekerSkillViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing JobSeekerSkill model operations with custom permission.
    """
    queryset = JobSeekerSkill.objects.all()
    serializer_class = JobSeekerSkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
