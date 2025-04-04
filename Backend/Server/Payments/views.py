from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils import timezone


from rest_framework.views import APIView, Response
from rest_framework import permissions, status

from Orders.models import SubscriptionOrder
from Subscriptions.models import AdvertisementSubscription, SubscriptionPlan

import requests
import json


#? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'



ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required

CallbackURL = 'http://127.0.0.1:8080/payments/verify/'


class SendPaymentRequest(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(SubscriptionOrder, order_id=order_id)

        request.session['order_id'] = str(order_id)

        if order.owner == request.user:
            data = {
                "MerchantID": settings.MERCHANT,
                "Amount": order.total_price,
                "Description": description,
                "CallbackURL": CallbackURL,
                "metadata": {
                    "Email": request.user.email,
                    "mobile": request.user.phone,
                    "order_id": order_id
                },
            }

            data = json.dumps(data)

            headers = {'content-type': 'application/json', 'content-length': str(len(data))}

            try:
                response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

                if response.status_code == 200:
                    response = response.json()
                    if response['Status'] == 100:
                        return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
                    else:
                        return {'status': False, 'code': str(response['Status'])}
                return response
        
            except requests.exceptions.Timeout:
                return {'status': False, 'code': 'timeout'}
            except requests.exceptions.ConnectionError:
                return {'status': False, 'code': 'connection error'}
        else:
            return Response({"Massage": "You dont have the permission to pay for this order."}, status=status.HTTP_403_FORBIDDEN)



class VerifyPaymentRequest(APIView):

    def get(self, request, authority):

        order_id = request.session['order_id']

        order = get_object_or_404(SubscriptionOrder, order_id=order_id)

        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.total_price,
            "Authority": authority,
        }
        
        data = json.dumps(data)
        
        # set content length by data
        
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        
        response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

        if response.status_code == 200:

            response = response.json()

            if response['Status'] == 100:
                
                try:
                    plan = SubscriptionPlan.objects.get(id=order.plan__id)
                    subscription = AdvertisementSubscription.objects.get(id=order.advertisement_subscription__id)
                    
                    now = timezone.now()
                    end_date = now + timezone.timedelta(order.durations)

                    subscription.subscription_status = 'special'
                    subscription.plan = plan
                    subscription.duration = order.durations

                    subscription.start_date = now
                    subscription.end_date = end_date

                    subscription.save()

                    order.payment_status = 'paid'
                    order.save()
                    
                except:
                    order.payment_status = 'failed'
                    order.save()
                    return Response({"Massage": "The Oprations faild"})
            else:
                order.payment_status = 'failed'
                order.save()
                return Response({"Massage": "Payment faild."}, status=status.HTTP_417_EXPECTATION_FAILED)