from rest_framework import serializers  # وارد کردن ماژول سریالایزرهای Django REST Framework
from .models import JobSeekerResume, Experience, Education, JobSeekerSkill  # ایمپورت مدل‌های مرتبط از فایل models




# ----------------------------
# سریالایزر رزومه جوینده کار
# ----------------------------
class JobSeekerResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerResume  # تعیین مدل مرتبط: رزومه جوینده کار
        fields = [
            'id', 'job_seeker_profile', 'industry', 'headline', 'bio', 'website', 'linkedin_profile',
            'location', 'gender', 'soldier_status', 'degree', 'years_of_experience',
            'experience', 'expected_salary', 'preferred_job_type', 'cv', 'availability',
            'created_at', 'updated_at'
        ]  # تعریف فیلدهای مورد استفاده در خروجی
        read_only_fields = ['job_seeker_profile', 'created_at', 'updated_at']  # فیلدهایی که فقط خواندنی هستند

    def update(self, instance, validated_data):
        """
        جلوگیری از به‌روزرسانی فیلدهای تغییرناپذیر مانند job_seeker_profile.
        """
        # اگر کاربر سعی کند فیلد job_seeker_profile را به‌روزرسانی کند، خطا می‌دهد.
        if 'job_seeker_profile' in validated_data:
            raise serializers.ValidationError(
                {"job_seeker_profile": "شما اجازه به‌روزرسانی پروفایل جوینده کار را ندارید."}
            )
        # به‌روزرسانی سایر فیلدهای مجاز به صورت پیش‌فرض  
        return super().update(instance, validated_data)


# ----------------------------
# سریالایزر تجربه کاری رزومه
# ----------------------------
class ExperienceSerializer(serializers.ModelSerializer):
    # تعریف فیلد "resume_id" به صورت write-only برای دریافت شناسه رزومه هنگام ایجاد
    resume_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Experience  # مدل مرتبط: تجربه کاری
        fields = [
            'id', 'resume', 'resume_id', 'employment_type', 'title', 'company', 'location',
            'start_date', 'end_date', 'description'
        ]  # فهرست فیلدهای استفاده شده
        read_only_fields = ['resume']  # فیلد resume به صورت read_only است، چرا که از resume_id مقداردهی می‌شود

    def create(self, validated_data):
        # استخراج شناسه رزومه از داده‌های ورودی
        resume_id = validated_data.pop('resume_id')
        try:
            # تلاش برای دریافت رزومه مربوطه با استفاده از شناسه
            resume = JobSeekerResume.objects.get(id=resume_id)
            validated_data['resume'] = resume  # افزودن رزومه به داده‌های اعتبارسنجی شده
        except JobSeekerResume.DoesNotExist:
            # در صورت عدم وجود رزومه با شناسه داده شده، خطا بازگردانی می‌شود
            raise serializers.ValidationError(
                {"resume_id": "رزومه با شناسه داده شده موجود نمی‌باشد."}
            )
        # ایجاد نمونه جدید با داده‌های معتبر
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # جلوگیری از به‌روزرسانی فیلد resume و استفاده از به‌روزرسانی پیشفرض سایر فیلدها
        return super().update(instance, validated_data)


# ----------------------------
# سریالایزر تحصیلات رزومه
# ----------------------------
class EducationSerializer(serializers.ModelSerializer):
    # تعریف فیلد "resume_id" به صورت write-only جهت دریافت شناسه رزومه هنگام ایجاد
    resume_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Education  # مدل مرتبط: تحصیلات
        fields = [
            'id', 'resume', 'resume_id', 'school', 'degree', 'grade', 'field_of_study',
            'start_date', 'end_date', 'description'
        ]
        read_only_fields = ['resume']  # فیلد رزومه فقط خواندنی است

    def create(self, validated_data):
        # استخراج resume_id و افزودن شیء رزومه به داده‌های ورودی
        resume_id = validated_data.pop('resume_id')
        try:
            resume = JobSeekerResume.objects.get(id=resume_id)
            validated_data['resume'] = resume
        except JobSeekerResume.DoesNotExist:
            raise serializers.ValidationError(
                {"resume_id": "رزومه با شناسه داده شده موجود نمی‌باشد."}
            )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # جلوگیری از به‌روزرسانی فیلد رزومه و اعمال به‌روزرسانی روی سایر فیلدها
        return super().update(instance, validated_data)


# ----------------------------
# سریالایزر مهارت رزومه جوینده کار
# ----------------------------
class JobSeekerSkillSerializer(serializers.ModelSerializer):
    # تعریف فیلد "resume_id" به صورت write-only جهت دریافت شناسه رزومه هنگام ایجاد
    resume_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = JobSeekerSkill  # مدل مرتبط: مهارت‌های رزومه جوینده کار
        fields = [
            'id', 'resume', 'resume_id', 'skill', 'level'
        ]
        read_only_fields = ['resume']  # فیلد resume قابل ویرایش نیست

    def create(self, validated_data):
        # استخراج شناسه رزومه از داده‌های ورودی
        resume_id = validated_data.pop('resume_id')
        try:
            resume = JobSeekerResume.objects.get(id=resume_id)
            validated_data['resume'] = resume  # افزودن رزومه به داده‌های معتبر شده
        except JobSeekerResume.DoesNotExist:
            raise serializers.ValidationError(
                {"resume_id": "رزومه با شناسه داده شده موجود نمی‌باشد."}
            )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # جلوگیری از به‌روزرسانی فیلد رزومه و استفاده از به‌روزرسانی پیش‌فرض برای بقیه‌ی فیلدها
        return super().update(instance, validated_data)
