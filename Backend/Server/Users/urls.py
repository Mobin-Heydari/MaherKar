# ایمپورت ماژول‌های ضروری از django.urls:
# - path: برای تعریف الگوهای URL
# - include: برای درج کردن URLهای تعریف‌شده در فایل‌ها یا ماژول‌های دیگر
from django.urls import path, include

# ایمپورت روترهای سفارشی تعریف‌شده در ماژول routers؛
# UserRouter: شامل URLهای مرتبط با مدیریت کاربران
# IdCardRouter: شامل URLهای مرتبط با اطلاعات کارت ملی
from .routers import UserRouter, IdCardRouter

# تعریف نام برنامه که به عنوان namespace در URLها استفاده می‌شود
app_name = "Users"

# ایجاد نمونه از روتر کاربران؛ این نمونه شامل الگوهای URL مربوط به UserViewSet می‌باشد
user_router = UserRouter()

# ایجاد نمونه از روتر اطلاعات کارت ملی؛ این نمونه شامل الگوهای URL مربوط به IdCardViewSet می‌باشد
id_card_router = IdCardRouter()

# تعریف الگوهای URL اصلی این برنامه
urlpatterns = [
    # مسیر 'user/' شامل URLهای تعریف‌شده در روتر کاربران؛
    # get_urls() متد سفارشی بازگردانی URLهای مربوط به عملیات CRUD کاربران است
    path('user/', include(user_router.get_urls())),
    
    # مسیر 'id-card/' شامل URLهای تعریف‌شده در روتر اطلاعات کارت ملی؛
    # get_urls() متد سفارشی بازگردانی URLهای مربوط به عملیات روی اطلاعات کارت ملی است
    path('id-card/', include(id_card_router.get_urls())),
]
