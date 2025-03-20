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




class JobSeekerProfileViewSet(viewsets.ModelViewSet):
    """
    ویوست برای مدیریت عملیات پروفایل جویندگان کار
    """

    # تعریف queryset برای ویوست
    queryset = JobSeekerProfile.objects.all()
    # تعریف کلاس سریالایزر برای ویوست
    serializer_class = JobSeekerProfileSerializer
    # تعریف کلاس‌های دسترسی برای ویوست
    permission_classes = [IsAuthenticated]
    # مشخص کردن فیلد برای متدهای بازیابی (retrieve)
    lookup_field = 'user__username'

    # متد لیست برای بازیابی لیست جویندگان کار
    def list(self, request, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت لیست پروفایل‌های جویندگان کار
        """
        try:
            if request.user.is_staff:
                queryset = self.get_queryset()
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # متد بازیابی برای مشاهده جزئیات یک جوینده کار
    def retrieve(self, request, user__username, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت اطلاعات یک پروفایل جوینده کار
        """
        try:
            if request.user.is_staff or request.user.username == user__username:
                profile = get_object_or_404(JobSeekerProfile, user__username=user__username)
                serializer = self.get_serializer(profile)
                return Response(serializer.data)
            else:
                return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)
        except JobSeekerProfile.DoesNotExist:
            return Response({"error": "پروفایل جوینده کار پیدا نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class EmployerProfileViewSet(viewsets.ModelViewSet):
    """
    ویوست برای مدیریت عملیات پروفایل کارفرما
    """

    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user__username'

    def list(self, request, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت لیست پروفایل‌های کارفرما
        """
        try:
            if request.user.is_staff:
                queryset = self.get_queryset()
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, user__username, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت اطلاعات یک پروفایل کارفرما
        """
        try:
            if request.user.is_staff or request.user.username == user__username:
                profile = get_object_or_404(EmployerProfile, user__username=user__username)
                serializer = self.get_serializer(profile)
                return Response(serializer.data)
            else:
                return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)
        except EmployerProfile.DoesNotExist:
            return Response({"error": "پروفایل کارفرما پیدا نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AdminProfileViewSet(viewsets.ModelViewSet):
    """
    ویوست برای مدیریت عملیات پروفایل مدیر
    """

    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user__username'

    def list(self, request, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت لیست پروفایل‌های مدیر
        """
        try:
            if request.user.is_superuser:  # فقط مدیران ارشد
                queryset = self.get_queryset()
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, user__username, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت اطلاعات یک پروفایل مدیر
        """
        try:
            if request.user.is_superuser:  # فقط مدیران ارشد
                profile = get_object_or_404(AdminProfile, user__username=user__username)
                serializer = self.get_serializer(profile)
                return Response(serializer.data)
            else:
                return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)
        except AdminProfile.DoesNotExist:
            return Response({"error": "پروفایل مدیر پیدا نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SupportProfileViewSet(viewsets.ModelViewSet):
    """
    ویوست برای مدیریت عملیات پروفایل پشتیبان
    """

    queryset = SupportProfile.objects.all()
    serializer_class = SupportProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user__username'

    def list(self, request, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت لیست پروفایل‌های پشتیبان
        """
        try:
            if request.user.is_staff:  # دسترسی فقط برای استاف‌ها
                queryset = self.get_queryset()
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, user__username, *args, **kwargs):
        """
        مدیریت درخواست‌های GET برای دریافت اطلاعات یک پروفایل پشتیبان
        """
        try:
            if request.user.is_staff:  # دسترسی فقط برای استاف‌ها
                profile = get_object_or_404(SupportProfile, user__username=user__username)
                serializer = self.get_serializer(profile)
                return Response(serializer.data)
            else:
                return Response({"error": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)
        except SupportProfile.DoesNotExist:
            return Response({"error": "پروفایل پشتیبان پیدا نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
