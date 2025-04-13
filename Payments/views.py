from django.shortcuts import get_object_or_404  
# ایمپورت تابع get_object_or_404 برای واکشی شیء از دیتابیس یا بازگرداندن خطای 404 در صورت عدم وجود

from django.conf import settings  
# ایمپورت تنظیمات پروژه برای استفاده از مقادیر پیکربندی مانند MERCHANT و SANDBOX

from django.utils import timezone  
# ایمپورت timezone برای کار با تاریخ و زمان در زمان‌بندی

from rest_framework.views import APIView, Response  
# ایمپورت کلاس APIView برای ایجاد ویو کلاس‌بیس و Response برای ارسال پاسخ‌های HTTP

from rest_framework import permissions, status  
# ایمپورت permissions برای مدیریت دسترسی و status برای کدهای وضعیت HTTP

from Orders.models import SubscriptionOrder  
# ایمپورت مدل SubscriptionOrder از اپ سفارشات جهت مدیریت سفارشات مرتبط با پرداخت

from Subscriptions.models import AdvertisementSubscription, SubscriptionPlan  
# ایمپورت مدل‌های AdvertisementSubscription و SubscriptionPlan از اپ اشتراک‌ها

import requests  
# ایمپورت کتابخانه requests برای ارسال درخواست‌های HTTP به درگاه پرداخت

import json  
# ایمپورت کتابخانه json برای تبدیل داده‌ها به فرمت JSON



# ---------------------------------------------------------------------------
# تنظیمات پرداخت Zarinpal
# ---------------------------------------------------------------------------
# تعیین آدرس درگاه پرداخت بر اساس حالت SANDBOX
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

# URL برای ارسال درخواست پرداخت
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"

# URL برای تایید تراکنش
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"

# URL برای شروع پرداخت
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # توضیحات مربوط به تراکنش (ضروری)

CallbackURL = 'http://127.0.0.1:8080/payments/verify/'  # آدرس بازگشت پس از پرداخت


# =============================================================================
# کلاس SendPaymentRequest: مدیریت ارسال درخواست پرداخت
# =============================================================================
class SendPaymentRequest(APIView):
    """
    ویو برای ارسال درخواست پرداخت به درگاه Zarinpal.
    """

    permission_classes = [permissions.IsAuthenticated]  
    # تنها کاربران احراز هویت‌شده می‌توانند به این ویو دسترسی داشته باشند

    def get(self, request, order_id):
        """
        ارسال درخواست پرداخت برای یک سفارش خاص.
        """
        # واکشی سفارش بر اساس order_id؛ بازگرداندن خطای 404 در صورت عدم وجود سفارش
        order = get_object_or_404(SubscriptionOrder, order_id=order_id)

        # ذخیره شناسه سفارش در session کاربر
        request.session['order_id'] = str(order_id)

        # بررسی مالکیت سفارش؛ فقط مالک سفارش می‌تواند پرداخت کند
        if order.owner == request.user:
            # داده‌های مورد نیاز برای ارسال درخواست به درگاه Zarinpal
            data = {
                "MerchantID": settings.MERCHANT,  # شناسه پذیرنده
                "Amount": order.total_price,  # مبلغ پرداخت
                "Description": description,  # توضیحات تراکنش
                "CallbackURL": CallbackURL,  # آدرس بازگشت پس از پرداخت
                "metadata": {
                    "Email": request.user.email,  # ایمیل کاربر
                    "mobile": request.user.phone,  # شماره تلفن کاربر
                    "order_id": order_id  # شناسه سفارش
                },
            }

            data = json.dumps(data)  # تبدیل داده‌ها به فرمت JSON

            # تنظیم هدر درخواست HTTP
            headers = {'content-type': 'application/json', 'content-length': str(len(data))}

            try:
                # ارسال درخواست پرداخت به Zarinpal
                response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

                if response.status_code == 200:  # بررسی وضعیت موفقیت‌آمیز بودن پاسخ
                    response = response.json()
                    if response['Status'] == 100:  # وضعیت موفقیت درخواست
                        # بازگرداندن آدرس شروع پرداخت و کد Authority
                        return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
                    else:
                        # بازگرداندن کد وضعیت خطای Zarinpal
                        return {'status': False, 'code': str(response['Status'])}
                return response

            except requests.exceptions.Timeout:
                # مدیریت خطای تایم‌اوت
                return {'status': False, 'code': 'timeout'}
            except requests.exceptions.ConnectionError:
                # مدیریت خطای اتصال
                return {'status': False, 'code': 'connection error'}
        else:
            # در صورت نداشتن مجوز پرداخت، بازگرداندن خطای دسترسی
            return Response({"Massage": "شما برای پرداخت این سفارش مجوز ندارین"}, status=status.HTTP_403_FORBIDDEN)


# =============================================================================
# کلاس VerifyPaymentRequest: مدیریت تایید تراکنش پرداخت
# =============================================================================
class VerifyPaymentRequest(APIView):
    """
    ویو برای تایید تراکنش پرداخت و به‌روزرسانی وضعیت سفارش و اشتراک.
    """

    def get(self, request, authority):
        """
        تایید تراکنش پرداخت با استفاده از Authority کد.
        """
        # دریافت شناسه سفارش از session
        order_id = request.session['order_id']

        # واکشی سفارش بر اساس order_id؛ بازگرداندن خطای 404 در صورت عدم وجود
        order = get_object_or_404(SubscriptionOrder, order_id=order_id)

        # داده‌های مورد نیاز برای تایید پرداخت
        data = {
            "MerchantID": settings.MERCHANT,  # شناسه پذیرنده
            "Amount": order.total_price,  # مبلغ تراکنش
            "Authority": authority,  # کد Authority برای تایید تراکنش
        }

        data = json.dumps(data)  # تبدیل داده‌ها به فرمت JSON

        # تنظیم هدر درخواست HTTP
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}

        # ارسال درخواست تایید پرداخت به Zarinpal
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:  # بررسی موفقیت‌آمیز بودن پاسخ
            response = response.json()

            if response['Status'] == 100:  # تایید موفقیت‌آمیز تراکنش
                try:
                    # واکشی طرح اشتراک و اشتراک آگهی مرتبط با سفارش
                    plan = SubscriptionPlan.objects.get(id=order.plan__id)
                    subscription = AdvertisementSubscription.objects.get(id=order.advertisement_subscription__id)

                    now = timezone.now()  # تاریخ فعلی
                    end_date = now + timezone.timedelta(order.durations)  # محاسبه تاریخ پایان اشتراک

                    # به‌روزرسانی اطلاعات اشتراک
                    subscription.subscription_status = 'special'
                    subscription.plan = plan
                    subscription.duration = order.durations
                    subscription.start_date = now
                    subscription.end_date = end_date

                    subscription.save()  # ذخیره تغییرات اشتراک

                    # به‌روزرسانی وضعیت پرداخت سفارش به 'paid'
                    order.payment_status = 'paid'
                    order.save()

                except:
                    # در صورت بروز خطا، تنظیم وضعیت پرداخت به 'failed'
                    order.payment_status = 'failed'
                    order.save()
                    return Response({"Massage": "عملیات موفق آمیز نبود."})

            else:
                # در صورت ناموفق بودن تایید تراکنش، به‌روزرسانی وضعیت پرداخت به 'failed'
                order.payment_status = 'failed'
                order.save()
                return Response({"Massage": "پرداخت با شکست مواجه شد."}, status=status.HTTP_417_EXPECTATION_FAILED)
