from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from rest_framework.generics import get_object_or_404

from .models import JobAdvertisement, Application, JobseekerResumeAdvertisement
from .serializers import JobAdvertisementSerializer, ApplicationSerializer, JobseekerResumeAdvertisementSerializer

from Resumes.models import JobSeekerResume



class JobAdvertisementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing JobAdvertisement model operations.
    """
    queryset = JobAdvertisement.objects.all()
    serializer_class = JobAdvertisementSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "slug"

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None, *args, **kwargs):
        queryset = get_object_or_404(self.get_queryset(), slug=slug)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Handles foreign key relationships in the serializer
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, slug=None, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), slug=slug)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, slug=None, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), slug=slug)
        instance.delete()
        return Response({"detail": "Advertisement deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



class ApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Application model operations.
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
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
        serializer.save()  # Automatically handles job seeker linkage in the serializer
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
        return Response({"detail": "Application deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



class JobseekerResumeAdvertisementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing JobseekerResumeAdvertisement objects.
    Only advertisements for the authenticated user's job seeker profile are accessible.
    Uses `slug` as the lookup field instead of the primary key.
    """
    queryset = JobseekerResumeAdvertisement.objects.all()
    serializer_class = JobseekerResumeAdvertisementSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "slug"

    def list(self, request, *args, **kwargs):
        """
        List all JobseekerResumeAdvertisement objects for the authenticated user.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None, *args, **kwargs):
        """
        Retrieve a specific advertisement instance using its slug.
        """
        advertisement = get_object_or_404(self.get_queryset(), slug=slug)
        serializer = self.get_serializer(advertisement)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new JobseekerResumeAdvertisement.
        The view expects the jobseeker's resume to be accessible via the user's jobseeker profile.
        This resume is passed in the serializer context so that fields such as gender,
        soldier status, degree, experience, salary, industry, and location are auto-populated.
        """
        try:
            resume = request.user.jobseekerprofile.Resume
        except (AttributeError, JobSeekerResume.DoesNotExist):
            return Response(
                {"detail": "No resume found for the current user."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data, context={"resume": resume})
        serializer.is_valid(raise_exception=True)
        serializer.save()  # The serializer's create method handles field auto-population.
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, slug=None, *args, **kwargs):
        """
        Update an existing advertisement (by slug).
        For partial updates, only fields like title and description are allowed;
        auto-populated fields remain unchanged.
        """
        advertisement = get_object_or_404(self.get_queryset(), slug=slug)
        serializer = self.get_serializer(advertisement, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, slug=None, *args, **kwargs):
        """
        Delete an advertisement using its slug.
        """
        advertisement = get_object_or_404(self.get_queryset(), slug=slug)
        advertisement.delete()
        return Response(
            {"detail": "Advertisement deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
