from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import (
    ReportCategory,
    EmployerReport,
    JobSeekerReport,
    AdvertisementReport
)
from .serializers import (
    ReportCategorySerializer,
    EmployerReportSerializer,
    JobSeekerReportSerializer,
    AdvertisementReportSerializer
)

from .permissions import IsAdminOrSupporterOrReporter, IsAdminOrReadOnly

from Users.models import User
from Advertisements.models import Advertisement



class ReportCategoryViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        queryset = ReportCategory.objects.all()
        serializer = ReportCategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        instance = get_object_or_404(ReportCategory, id=pk)
        serializer = ReportCategorySerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = ReportCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'The category is created.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        instance = get_object_or_404(ReportCategory, id=pk)
        serializer = ReportCategorySerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'The category updated.'}, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        insatnce = get_object_or_404(ReportCategory, id=pk)
        insatnce.delete()
        return Response({'message': 'The category is deleted.'}, status=status.HTTP_204_NO_CONTENT)




class JobSeekerReportViewSet(viewsets.ViewSet):
    """
    ویوست برای مدیریت گزارش‌های جویندگان کار.
    """
    permission_classes = [IsAuthenticated, IsAdminOrSupporterOrReporter]
    lookup_field = 'pk'

    def list(self, request, *args, **kwargs):
        """
        لیست تمامی گزارش‌ها؛ فقط قابل دسترسی توسط مدیران (admin).
        """
        queryset = JobSeekerReport.objects.all()
        serializer = JobSeekerReportSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk, *args, **kwargs):
        """
        دریافت جزئیات یک گزارش؛ قابل دسترسی توسط مدیران، گزارش‌دهنده، یا جوینده کار گزارش‌شده.
        """
        instance = get_object_or_404(JobSeekerReport, id=pk)
        serializer = JobSeekerReportSerializer(instance)
        return Response(serializer.data)
    

    def create(self, request, pk, *args, **kwargs):
        if pk is None:
            return Response({"message":"The user id is needed."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, id=pk)

        if user.user_type != "JS":
            return Response({'error': 'This user is not a jobseeker'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        serializer = JobSeekerReportSerializer(data=request.data, context={'request': request, 'user_id': user.id})
        if serializer.is_valid():
            serializer.save()
            return Response({'massage': 'The report created.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        """
        بروزرسانی یک گزارش موجود؛ فقط توسط مدیران یا گزارش‌دهنده قابل انجام است.
        """
        instance = get_object_or_404(JobSeekerReport, id=pk)
        self.check_object_permissions(request, instance)
        serializer = JobSeekerReportSerializer(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, *args, **kwargs):
        """
        حذف یک گزارش؛ فقط توسط مدیران یا گزارش‌دهنده قابل انجام است.
        """
        instance = get_object_or_404(JobSeekerReport, id=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response({"message": "گزارش حذف شد"}, status=status.HTTP_204_NO_CONTENT)


class EmployerReportViewSet(viewsets.ViewSet):
    """
    ویوست برای مدیریت گزارش‌های کارفرماها.
    """
    permission_classes = [IsAuthenticated, IsAdminOrSupporterOrReporter]
    lookup_field = 'pk'

    def list(self, request, *args, **kwargs):
        """
        لیست تمامی گزارش‌ها؛ فقط قابل دسترسی توسط مدیران (admin).
        """
        queryset = EmployerReport.objects.all()
        serializer = EmployerReportSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk, *args, **kwargs):
        """
        دریافت جزئیات یک گزارش؛ قابل دسترسی توسط مدیران، گزارش‌دهنده، یا جوینده کار گزارش‌شده.
        """

        instance = get_object_or_404(EmployerReport, id=pk)
        serializer = EmployerReportSerializer(instance)
        return Response(serializer.data)

    def create(self, request, pk, *args, **kwargs):
        if pk is None:
            return Response({"message":"The user id is needed."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, id=pk)
        if user.user_type != "EM":
            return Response({'error': 'This user is not a jobseeker'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        serializer = EmployerReportSerializer(data=request.data, context={'request': request, 'user_id': user.id})
        if serializer.is_valid():
            serializer.save()
            return Response({'massage': 'The report created.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        """
        بروزرسانی یک گزارش موجود؛ فقط توسط مدیران یا گزارش‌دهنده قابل انجام است.
        """
        instance = get_object_or_404(EmployerReport, id=pk)
        self.check_object_permissions(request, instance)
        serializer = EmployerReportSerializer(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, *args, **kwargs):
        """
        حذف یک گزارش؛ فقط توسط مدیران یا گزارش‌دهنده قابل انجام است.
        """
        instance = get_object_or_404(EmployerReport, id=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response({"message": "گزارش حذف شد"}, status=status.HTTP_204_NO_CONTENT)


class AdvertisementReportViewSet(viewsets.ViewSet):
    """
    ویوست برای مدیریت گزارش‌های آگهی‌ها.
    """
    permission_classes = [IsAuthenticated, IsAdminOrSupporterOrReporter]
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        queryset = AdvertisementReport.objects.all()
        serializer = AdvertisementReportSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(AdvertisementReport, id=pk)
        serializer = AdvertisementReportSerializer(instance)
        return Response(serializer.data)

    def create(self, request, pk, *args, **kwargs):
        if pk is None:
            return Response({"message":"The ad_id is needed."}, status=status.HTTP_400_BAD_REQUEST)
        
        advertisement = get_object_or_404(Advertisement, id=pk)
        serializer = AdvertisementReportSerializer(data=request.data, context={'request': request, 'ad_id': advertisement.id})
        if serializer.is_valid():
            serializer.save(reporter=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk, *args, **kwargs):
        """
        بروزرسانی یک گزارش موجود؛ فقط توسط مدیران یا گزارش‌دهنده قابل انجام است.
        """
        instance = get_object_or_404(AdvertisementReport, id=pk)
        self.check_object_permissions(request, instance)
        serializer = AdvertisementReportSerializer(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, pk, *args, **kwargs):
        """
        حذف یک گزارش؛ فقط توسط مدیران یا گزارش‌دهنده قابل انجام است.
        """
        instance = get_object_or_404(AdvertisementReport, id=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response({"message": "گزارش حذف شد"}, status=status.HTTP_204_NO_CONTENT)
