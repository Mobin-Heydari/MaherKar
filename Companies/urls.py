from django.urls import path, include  # ایمپورت توابع path و include جهت تعریف و درج URLها
from .routers import CompanyRouter      # ایمپورت روتر سفارشی تعریف‌شده برای مدیریت URLهای Company



app_name = "Companies"  # تعریف namespace برای اپلیکیشن شرکت‌ها جهت جلوگیری از تداخل نام‌های URL در کل پروژه



# ایجاد نمونه‌ای از روتر سفارشی شرکت
router = CompanyRouter()



# تعریف نهایی URLها به صورت ماژولار؛ تمامی URLهای ثبت‌شده در روتر به این الگو اضافه می‌شوند
urlpatterns = [
    path('', include(router.urls)),  # درج تمامی URLهای روتر در مسیر پایه‌ی اپ (برای مثال: /companies/)
]
