# ایمپورت ماژول‌های ضروری
from django.urls import path, include
from .routers import UserRouter

# تعریف نام برنامه
app_name = "Users"

# ایجاد یک نمونه از روت سفارشی
router = UserRouter()

# تعریف الگوهای URL برای این برنامه
urlpatterns = [
    # اضافه کردن URLهای روت سفارشی
    path('', include(UserRouter().urls)),  # شامل کردن URLهای روت کاربر
]
