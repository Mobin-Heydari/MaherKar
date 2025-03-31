from django.urls import path, include
from .routers import (
    SubscriptionPlanRouter,
    DurationRouter,
    JobAdvertisementSubscriptionRouter,
    JobseekerResumeAdvertisementSubscriptionRouter,
)


app_name = "Subscriptions"


subscription_plan_router = SubscriptionPlanRouter()
duration_router = DurationRouter()
job_ad_subscription_router = JobAdvertisementSubscriptionRouter()
resume_ad_subscription_router = JobseekerResumeAdvertisementSubscriptionRouter()



urlpatterns = [
    path('plans/', include(subscription_plan_router.get_urls())),
    path('durations/', include(duration_router.get_urls())),
    path('jobs/', include(job_ad_subscription_router.get_urls())),
    path('resumes/', include(resume_ad_subscription_router.get_urls()))
]
