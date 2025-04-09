from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import JobSeekerProfile, EmployerProfile, AdminProfile, SupportProfile
from .serializers import (
    JobSeekerProfileSerializer,
    EmployerProfileSerializer,
    AdminProfileSerializer,
    SupportProfileSerializer
)





class JobSeekerProfileViewSet(viewsets.ViewSet):
    """
    ویوست برای مدیریت عملیات پروفایل جویندگان کار
    """
    # تعریف کلاس‌های دسترسی برای ویوست
    permission_classes = [IsAuthenticated]
    # مشخص کردن فیلد برای متدهای بازیابی (retrieve)
    lookup_field = 'user__username'

    # متد لیست برای بازیابی لیست جویندگان کار
    def list(self, request, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت لیست پروفایل‌های جویندگان کار
        """
        if request.user.is_staff:
            queryset = JobSeekerProfile.objects.all()
            serializer = JobSeekerProfileSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    # متد بازیابی برای مشاهده جزئیات یک جوینده کار
    def retrieve(self, request, user__username, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت اطلاعات یک پروفایل جوینده کار
        """
        if request.user.is_staff or request.user.username == user__username:
            profile = get_object_or_404(JobSeekerProfile, user__username=user__username)
            serializer = JobSeekerProfileSerializer(profile)
            return Response(serializer.data)
        else:
            return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)
    
    def update(self, request, user__username):
        if request.user.is_staff or request.user.username == user__username:
            profile = get_object_or_404(JobSeekerProfile, user__username=user__username)
            serializer = JobSeekerProfileSerializer(profile, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "شما اجازه ویرایش این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)




class EmployerProfileViewSet(viewsets.ViewSet):
    """
    ویوست برای مدیریت عملیات پروفایل کارفرما
    """
    permission_classes = [IsAuthenticated]
    lookup_field = 'user__username'

    def list(self, request, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت لیست پروفایل‌های کارفرما
        """
        if request.user.is_staff:
            queryset = EmployerProfile.objects.all()
            serializer = EmployerProfileSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)


    def retrieve(self, request, user__username, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت اطلاعات یک پروفایل کارفرما
        """
        if request.user.is_staff or request.user.username == user__username:
            profile = get_object_or_404(EmployerProfile, user__username=user__username)
            serializer = EmployerProfileSerializer(profile)
            return Response(serializer.data)
        else:
            return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, user__username):
        if request.user.is_staff or request.user.username == user__username:
            profile = get_object_or_404(EmployerProfile, user__username=user__username)
            serializer = EmployerProfileSerializer(profile, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "شما اجازه ویرایش این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)




class AdminProfileViewSet(viewsets.ViewSet):
    """
    ویوست برای مدیریت عملیات پروفایل مدیر
    """

    permission_classes = [IsAuthenticated]
    lookup_field = 'user__username'

    def list(self, request, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت لیست پروفایل‌های مدیر
        """

        if request.user.is_superuser:  # فقط مدیران ارشد
            queryset = AdminProfile.objects.all()
            serializer = AdminProfileSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, user__username, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت اطلاعات یک پروفایل مدیر
        """
        if request.user.is_superuser:
            profile = get_object_or_404(AdminProfile, user__username=user__username)
            serializer = AdminProfileSerializer(profile)
            return Response(serializer.data)
        else:
            return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, user__username):
        if request.user.is_staff or request.user.username == user__username:
            profile = get_object_or_404(AdminProfile, user__username=user__username)
            serializer = AdminProfileSerializer(profile, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "شما اجازه ویرایش این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)



class SupportProfileViewSet(viewsets.ViewSet):
    """
    ویوست برای مدیریت عملیات پروفایل پشتیبان
    """

    permission_classes = [IsAuthenticated]
    lookup_field = 'user__username'


    def list(self, request, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت لیست پروفایل‌های پشتیبان
        """
        if request.user.is_staff:  # دسترسی فقط برای استاف‌ها
            queryset = SupportProfile.objects.all()
            serializer = SupportProfileSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)
    

    def retrieve(self, request, user__username, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت اطلاعات یک پروفایل پشتیبان
        """
        if request.user.is_staff:  # دسترسی فقط برای استاف‌ها
            profile = get_object_or_404(SupportProfile, user__username=user__username)
            serializer = SupportProfileSerializer(profile)
            return Response(serializer.data)
        else:
            return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)
    
    def update(self, request, user__username):
        if request.user.is_staff or request.user.username == user__username:
            profile = get_object_or_404(SupportProfile, user__username=user__username)
            serializer = SupportProfileSerializer(profile, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "شما اجازه ویرایش این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)

