from django.test import TestCase
from Profiles.models import JobSeekerProfile, EmployerProfile, AdminProfile, SupportProfile
from .models import User




class UserProfileCreationTest(TestCase):
    """
    تست برای بررسی ایجاد خودکار پروفایل هنگام ایجاد کاربر.
    """

    def test_job_seeker_profile_creation(self):
        """
        بررسی اینکه آیا پروفایل جوینده کار به درستی ایجاد می‌شود یا خیر.
        """
        # ایجاد یک کاربر جوینده کار
        user = User.objects.create_user(
            phone="09123456789",
            user_type="JS",
            password="password123",
            full_name="test3"
        )
        # بررسی وجود پروفایل مرتبط
        self.assertTrue(JobSeekerProfile.objects.filter(user=user).exists(), "پروفایل جوینده کار ایجاد نشد!")

    def test_employer_profile_creation(self):
        """
        بررسی اینکه آیا پروفایل کارفرما به درستی ایجاد می‌شود یا خیر.
        """
        # ایجاد یک کاربر کارفرما
        user = User.objects.create_user(
            phone="09111234567",
            user_type="EM",
            password="password123",
            full_name="test2"
        )
        # بررسی وجود پروفایل مرتبط
        self.assertTrue(EmployerProfile.objects.filter(user=user).exists(), "پروفایل کارفرما ایجاد نشد!")

    def test_admin_profile_creation(self):
        """
        بررسی اینکه آیا پروفایل مدیر به درستی ایجاد می‌شود یا خیر.
        """
        # ایجاد یک کاربر ادمین
        user = User.objects.create_superuser(
            phone="09134455678",
            password="adminpassword123",
            full_name="test"
        )
        # بررسی وجود پروفایل مرتبط
        self.assertTrue(AdminProfile.objects.filter(user=user).exists(), "پروفایل مدیر ایجاد نشد!")

    def test_support_profile_creation(self):
        """
        بررسی اینکه آیا پروفایل پشتیبان به درستی ایجاد می‌شود یا خیر.
        """
        # ایجاد یک کاربر پشتیبان
        user = User.objects.create_user(
            phone="09199887766",
            user_type="SU",
            password="password123",
            full_name="test1"
        )
        # بررسی وجود پروفایل مرتبط
        self.assertTrue(SupportProfile.objects.filter(user=user).exists(), "پروفایل پشتیبان ایجاد نشد!")
