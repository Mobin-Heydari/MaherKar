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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Handles job_seeker_profile linkage in the serializer
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        instance.delete()
        return Response({"detail": "Resume deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


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

    def create(self, request, *args, **kwargs):
        resume_id = request.data.get('resume_id')  # Get resume_id from the request data
        if not resume_id:
            return Response({"error": "resume_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            resume = JobSeekerResume.objects.get(id=resume_id)  # Ensure the resume exists
            request.data['resume'] = resume.id  # Add resume ID to the validated data
        except JobSeekerResume.DoesNotExist:
            return Response({"error": "Resume not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        instance.delete()
        return Response({"detail": "Experience deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


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

    def create(self, request, *args, **kwargs):
        resume_id = request.data.get('resume_id')  # Get resume_id from the request data
        if not resume_id:
            return Response({"error": "resume_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            resume = JobSeekerResume.objects.get(id=resume_id)  # Ensure the resume exists
            request.data['resume'] = resume.id  # Add resume ID to the validated data
        except JobSeekerResume.DoesNotExist:
            return Response({"error": "Resume not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        instance.delete()
        return Response({"detail": "Education deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


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

    def create(self, request, *args, **kwargs):
        resume_id = request.data.get('resume_id')  # Get resume_id from the request data
        if not resume_id:
            return Response({"error": "resume_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            resume = JobSeekerResume.objects.get(id=resume_id)  # Ensure the resume exists
            request.data['resume'] = resume.id  # Add resume ID to the validated data
        except JobSeekerResume.DoesNotExist:
            return Response({"error": "Resume not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        instance.delete()
        return Response({"detail": "Skill deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
