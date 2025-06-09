from rest_framework import serializers

from .models import (
    ReportCategory,
    JobSeekerReport,
    EmployerReport,
    AdvertisementReport,
)

from Users.serializers import UserSerializer
from Users.models import User
from Advertisements.serializers import AdvertisementSerializer
from Advertisements.models import Advertisement




class ReportCategorySerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدیریت دسته‌بندی گزارش‌ها.
    این کلاس فیلدهای شناسه، نام و توضیحات دسته‌بندی را فراهم می‌کند.
    """
    class Meta:
        model = ReportCategory
        fields = ['id', 'name', 'description']

    
    def create(self, validated_data):
        query = ReportCategory.objects.create(name=validated_data['name'], description=validated_data['description'])
        query.save()
        return query
    

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance



class JobSeekerReportSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدیریت گزارش‌های جویندگان کار.
    علاوه بر فیلدهای اصلی، نام کاربری جوینده و گزارش‌دهنده به‌صورت فقط خواندنی ارائه می‌شود.
    """

    category_id = serializers.CharField(write_only=True, required=True)
    category = ReportCategorySerializer(read_only=True)
    reported_jobseeker = UserSerializer(read_only=True)
    reporter = UserSerializer(read_only=True)

    class Meta:
        model = JobSeekerReport
        fields = [
            'id',
            'status',
            'reported_jobseeker',
            'reporter',
            'category_id',
            'category',
            'description',
            'created_at',
        ]
        read_only_fields = ['category', 'reported_jobseeker', 'reporter']

    def create(self, validated_data):

        user_id = self.context.get('user_id')
        request = self.context.get("request")

        category_id = validated_data.pop("category_id", None)
        if category_id is not None:
            try:
                category = ReportCategory.objects.get(id=category_id)
            except ReportCategory.DoesNotExist:
                raise serializers.ValidationError({"category_id": "City with the specified ID does not exist."})
        else:
            raise serializers.ValidationError({"category_id": "The 'category_id' field is required for creating a company."})
        
        reporter = request.user
        reported_jobseeker = User.objects.get(id=user_id)

        if 'description' not in validated_data:
            raise serializers.ValidationError({'description': 'this field is required.'})

        query = JobSeekerReport.objects.create(
            category=category,
            reported_jobseeker=reported_jobseeker,
            reporter=reporter,
            description=validated_data.get('description', None)
        )

        query.save()

        return query



    def update(self, instance, validated_data):
        """
        به‌روزرسانی وضعیت و توضیحات گزارش جویندگان کار.
        اگر داده‌های جدید ارسال شوند، مقدار آن‌ها جایگزین می‌شوند.
        """
        request = self.context.get('request')
        user = request.user

        if user.is_staff or user.user_type == 'SU':
            instance.status = validated_data.get('status', instance.status)

        if user == instance.reporter:
            instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance



class EmployerReportSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدیریت گزارش‌های مربوط به کارفرمایان.
    اطلاعات کاربری گزارش شده و گزارش‌دهنده در فیلدهای فقط خواندنی نمایش داده می‌شوند.
    """
    category_id = serializers.CharField(write_only=True, required=True)
    category = ReportCategorySerializer(read_only=True)
    reported_employer = UserSerializer(read_only=True)
    reporter = UserSerializer(read_only=True)

    class Meta:
        model = EmployerReport
        fields = [
            'id',
            'status',
            'category_id',
            'reported_employer',
            'reporter',
            'category',
            'description',
            'created_at',
        ]
        read_only_fields = ['category', 'reported_employer', 'reporter']

    def create(self, validated_data):

        user_id = self.context.get('user_id')
        request = self.context.get("request")

        category_id = validated_data.pop("category_id", None)
        if category_id is not None:
            try:
                category = ReportCategory.objects.get(id=category_id)
            except ReportCategory.DoesNotExist:
                raise serializers.ValidationError({"category_id": "City with the specified ID does not exist."})
        else:
            raise serializers.ValidationError({"category_id": "The 'category_id' field is required for creating a company."})
        
        reporter = request.user
        reported_employer = User.objects.get(id=user_id)

        if 'description' not in validated_data:
            raise serializers.ValidationError({'description': 'this field is required.'})

        query = EmployerReport.objects.create(
            category=category,
            reported_employer=reported_employer,
            reporter=reporter,
            description=validated_data.get('description', None)
        )

        query.save()

        return query



    def update(self, instance, validated_data):
        """
        به‌روزرسانی وضعیت و توضیحات گزارش جویندگان کار.
        اگر داده‌های جدید ارسال شوند، مقدار آن‌ها جایگزین می‌شوند.
        """
        request = self.context.get('request')
        user = request.user

        if user.is_staff or user.user_type == 'SU':
            instance.status = validated_data.get('status', instance.status)

        if user == instance.reporter:
            instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance


class AdvertisementReportSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدیریت گزارش‌های مربوط به آگهی‌ها.
    نام کاربری گزارش‌دهنده به عنوان فیلد فقط خواندنی ارائه می‌شود.
    """
    reporter = UserSerializer(read_only=True)
    advertisement = AdvertisementSerializer(read_only=True)
    category = ReportCategorySerializer(read_only=True)
    
    category_id = serializers.CharField(write_only=True, required=False)



    class Meta:
        model = AdvertisementReport
        fields = [
            'id',
            'status',
            'advertisement',
            'category_id',
            'reporter',
            'category',
            'description',
            'created_at',
        ]

        read_only_fields = ['advertisement', 'reporter', 'category']

    def create(self, validated_data):
        """
        ایجاد یک گزارش جدید برای آگهی‌ها.
        """

        request = self.context.get("request")
        ad_id = self.context.get('ad_id')


        advertisement = Advertisement.objects.get(id=ad_id)


        category_id = validated_data.pop("category_id", None)
        if category_id is not None:
            try:
                category = ReportCategory.objects.get(id=category_id)
            except ReportCategory.DoesNotExist:
                raise serializers.ValidationError({"category_id": "City with the specified ID does not exist."})
        else:
            raise serializers.ValidationError({"category_id": "The 'category_id' field is required for creating a company."})
        
        if 'description' not in validated_data:
            raise serializers.ValidationError({'description': 'this field is required.'})

        query = AdvertisementReport.objects.create(
            advertisement=advertisement,
            reporter=request.user,
            category=category,
            description=validated_data['description']
        )

        query.save()
        return query


    def update(self, instance, validated_data):
        """
        به‌روزرسانی وضعیت و توضیحات گزارش مربوط به آگهی.
        """
        request = self.context.get('request')
        user = request.user

        if user.is_staff or user.user_type == 'SU':
            instance.status = validated_data.get('status', instance.status)

        if user == instance.reporter:
            instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance
