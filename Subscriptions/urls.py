from django.urls import path, include  
# ایمپورت توابع path و include برای تعریف و درج URLها

from .routers import SubscriptionPlanRouter, AdvertisementSubscriptionRouter  
# ایمپورت روترهای سفارشی مربوط به طرح‌های اشتراک و اشتراک‌های آگهی از فایل routers



app_name = "Subscriptions"  
# تعریف فضای نام (namespace) برای اپلیکیشن اشتراک‌ها؛ این نامگذاری به جلوگیری از تداخل URLها در پروژه کمک می‌کند



# ایجاد نمونه‌هایی از روترهای سفارشی
subscription_plan_router = SubscriptionPlanRouter()
ad_subscription_router = AdvertisementSubscriptionRouter()



# تعریف مسیرهای URL اصلی
urlpatterns = [
    # مسیر 'plans/' شامل تمامی URLهای مربوط به طرح‌های اشتراک است؛
    # URLها از طریق متد get_urls() در subscription_plan_router درج می‌شوند.
    path('plans/', include(subscription_plan_router.get_urls())),

    # مسیر 'advertisement-subscription/' شامل تمامی URLهای مربوط به اشتراک‌های آگهی است؛
    # URLها از طریق متد get_urls() در ad_subscription_router درج می‌شوند.
    path('advertisement-subscription/', include(ad_subscription_router.get_urls()))
]
