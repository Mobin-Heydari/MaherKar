from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import (
    JobSeekerReport,
    EmployerReport,
    AdvertisementReport
)
from .serializers import (
    JobSeekerReportSerializer,
    EmployerReportSerializer,
    AdvertisementReportSerializer
)


class JobSeekerReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing JobSeeker reports.
    """
    queryset = JobSeekerReport.objects.all()
    serializer_class = JobSeekerReportSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        """
        List all JobSeeker reports. Only accessible by admin users.
        """
        if request.user.is_staff:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, id=None, *args, **kwargs):
        """
        Retrieve a specific JobSeeker report. Accessible by admin, reporter, or reported JobSeeker.
        """
        report = get_object_or_404(self.get_queryset(), id=id)
        if request.user.is_staff or request.user == report.reporter or request.user == report.reported_jobseeker.user:
            serializer = self.get_serializer(report)
            return Response(serializer.data)
        return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        """
        Create a new JobSeeker report.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reporter=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, id=None, *args, **kwargs):
        """
        Update an existing JobSeeker report. Only admin or the reporter can perform this action.
        """
        report = get_object_or_404(self.get_queryset(), id=id)
        if request.user.is_staff or request.user == report.reporter:
            serializer = self.get_serializer(report, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "شما اجازه به‌روزرسانی این گزارش را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, id=None, *args, **kwargs):
        """
        Delete a JobSeeker report. Only admin or the reporter can perform this action.
        """
        report = get_object_or_404(self.get_queryset(), id=id)
        if request.user.is_staff or request.user == report.reporter:
            report.delete()
            return Response({"message": "گزارش حذف شد"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "شما اجازه حذف این گزارش را ندارید"}, status=status.HTTP_403_FORBIDDEN)


class EmployerReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Employer reports.
    """
    queryset = EmployerReport.objects.all()
    serializer_class = EmployerReportSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        """
        List all Employer reports. Only accessible by admin users.
        """
        if request.user.is_staff:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, id=None, *args, **kwargs):
        """
        Retrieve a specific Employer report. Accessible by admin, reporter, or reported Employer.
        """
        report = get_object_or_404(self.get_queryset(), id=id)
        if request.user.is_staff or request.user == report.reporter or request.user == report.reported_employer.user:
            serializer = self.get_serializer(report)
            return Response(serializer.data)
        return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        """
        Create a new Employer report.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reporter=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, id=None, *args, **kwargs):
        """
        Update an existing Employer report. Only admin or the reporter can perform this action.
        """
        report = get_object_or_404(self.get_queryset(), id=id)
        if request.user.is_staff or request.user == report.reporter:
            serializer = self.get_serializer(report, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "شما اجازه به‌روزرسانی این گزارش را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, id=None, *args, **kwargs):
        """
        Delete an Employer report. Only admin or the reporter can perform this action.
        """
        report = get_object_or_404(self.get_queryset(), id=id)
        if request.user.is_staff or request.user == report.reporter:
            report.delete()
            return Response({"message": "گزارش حذف شد"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "شما اجازه حذف این گزارش را ندارید"}, status=status.HTTP_403_FORBIDDEN)


class JobAdvertisementReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Advertisement reports.
    """
    queryset = AdvertisementReport.objects.all()
    serializer_class = AdvertisementReportSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        """
        List all Advertisement reports. Only accessible by admin users.
        """
        if request.user.is_staff:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, id=None, *args, **kwargs):
        """
        Retrieve a specific Advertisement report. Accessible by admin or the reporter.
        """
        report = get_object_or_404(self.get_queryset(), id=id)
        if request.user.is_staff or request.user == report.reporter:
            serializer = self.get_serializer(report)
            return Response(serializer.data)
        return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        """
        Create a new Advertisement report.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reporter=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, id=None, *args, **kwargs):
        """
        Update an existing Advertisement report. Only admin or the reporter can perform this action.
        """
        report = get_object_or_404(self.get_queryset(), id=id)
        if request.user.is_staff or request.user == report.reporter:
            serializer = self.get_serializer(report, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "شما اجازه به‌روزرسانی این گزارش را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, id=None, *args, **kwargs):
        """
        Delete an Advertisement report. Only admin or the reporter can perform this action.
        """
        report = get_object_or_404(self.get_queryset(), id=id)
        if request.user.is_staff or request.user == report.reporter:
            report.delete()
            return Response({"message": "گزارش حذف شد"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "شما اجازه حذف این گزارش را ندارید"}, status=status.HTTP_403_FORBIDDEN)
