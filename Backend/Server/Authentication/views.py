from django.shortcuts import get_object_or_404  # ایمپورت برای دریافت شیء یا پرتاب خطای 404 اگر شیء یافت نشود
from rest_framework.views import APIView, Response  # ایمپورت کلاس APIView برای ایجاد ویو و Response برای پاسخ به درخواست‌ها
from rest_framework.permissions import IsAuthenticated  # ایمپورت مجوز برای احراز هویت کاربران
from rest_framework import status  # ایمپورت کد وضعیت برای پاسخ‌های HTTP

from rest_framework_simplejwt.tokens import RefreshToken  # ایمپورت برای ایجاد توکن JWT
from rest_framework.exceptions import ValidationError  # ایمپورت خطای اعتبارسنجی

from Users.models import User  # ایمپورت مدل کاربر از برنامه Users

from .serializers import LoginSerializer, UserRegisterOneTimePasswordSerializer, UserRegisterSerializer  # ایمپورت سریالایزرهای مربوطه
from .models import OneTimePassword, UserRegisterOTP  # ایمپورت مدل‌های رمز یکبار مصرف و ثبت‌نام

from kavenegar import KavenegarAPI, APIException, HTTPException

from Server.settings import KAVENEGAR_API_KEY



# تعریف یک ویو کلاس‌بیس برای مدیریت ورود کاربران
class LoginAPIView(APIView):
    """
    ویو ورود برای احراز هویت کاربران و بازگرداندن توکن JWT.
    """
    
    def post(self, request):  # متد POST برای مدیریت درخواست‌های ورود
        """
        مدیریت درخواست‌های POST برای ویو ورود.
        
        :param request: شیء درخواست دریافتی
        :return: شیء پاسخ با توکن‌های refresh و access
        """
        
        serializer = LoginSerializer(data=request.data)  # ایجاد یک نمونه از سریالایزر با داده‌های درخواست

        if request.user.is_authenticated:  # بررسی اینکه آیا کاربر قبلاً وارد شده است
            return Response({"message": "شما قبلاً وارد شده‌اید"}, status=status.HTTP_400_BAD_REQUEST)  # پاسخ خطا
        else:
            if serializer.is_valid():  # بررسی اعتبار سریالایزر
                phone = serializer.validated_data['phone']  # استخراج شماره تلفن از داده‌های تاییدشده
                user = User.objects.get(phone=phone)  # دریافت شیء کاربر از دیتابیس

                if not user.is_active:  # بررسی اینکه آیا کاربر فعال است
                    return Response({'error': 'کاربر فعال نیست'}, status=status.HTTP_401_UNAUTHORIZED)  # پاسخ خطا
                
                refresh = RefreshToken.for_user(user)  # ایجاد توکن refresh برای کاربر
                
                return Response(  # پاسخ موفق با توکن‌ها
                    {
                        'refresh': str(refresh), 
                        'access': str(refresh.access_token)
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # پاسخ خطا با جزئیات سریالایزر
    
    def handle_exception(self, exc):  # متد برای مدیریت استثناها
        """
        مدیریت استثناهایی که در طول اجرای ویو رخ می‌دهند.
        
        :param exc: شیء استثنا
        :return: شیء پاسخ با پیام خطا
        """
        
        if isinstance(exc, ValidationError):  # بررسی اینکه آیا استثنا خطای اعتبارسنجی است
            return Response({'error': 'خطای اعتبارسنجی'}, status=status.HTTP_400_BAD_REQUEST)  # پاسخ خطا
        return super().handle_exception(exc)  # مدیریت سایر استثناها با کلاس والد





# ویو برای مدیریت تولید رمز یکبار مصرف
class UserRegisterOtpAPIView(APIView):
    """
    ویو برای تولید رمز یکبار مصرف.
    """
    def post(self, request):  # متد POST برای درخواست رمز یکبار مصرف
        """
        مدیریت درخواست POST برای تولید رمز یکبار مصرف.
        """
        if not request.user.is_authenticated:  # بررسی اینکه آیا کاربر وارد نشده است

            serializer = UserRegisterOneTimePasswordSerializer(data=request.data)  # نمونه سریالایزر

            if serializer.is_valid(raise_exception=True):  # اعتبارسنجی داده‌ها

                otp_data = serializer.create(validated_data=serializer.validated_data)  # تولید رمز یکبار مصرف

                try:
                    api = KavenegarAPI(str(KavenegarAPI))
                    params = { 'sender': '2000660110', 'receptor': str(otp_data['phone']), 'message': f'به ماهر کار خوش آمدید لطفا کد ارسال شده را وارد کنید. {otp_data['code']}' }
                    response = api.sms_send(params)
                    print(response)
                except APIException as e: 
                    print(e)
                except HTTPException as e: 
                    print(e)

                return Response({  # پاسخ موفق با جزئیات رمز
                    'Detail': {
                        'Message': 'Otp created successfully',
                        'token': otp_data['token'], 
                        'code': otp_data['code'] 
                    }
                }, status=status.HTTP_201_CREATED)
            
            else:
                return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  # پاسخ خطا
        else:
            return Response({'Detail': 'You are already logged in'}, status=status.HTTP_400_BAD_REQUEST)  # پاسخ خطا اگر کاربر وارد شده باشد


# ویو برای مدیریت ثبت‌نام کاربران با تایید رمز یکبار مصرف
class UserRegisterOtpValidateAPIView(APIView):
    """
    ویو برای ثبت‌نام کاربران با تایید رمز یکبار مصرف.
    """
    def post(self, request, token):  # متد POST برای ثبت‌نام کاربر
        """
        مدیریت درخواست POST برای ثبت‌نام و تایید رمز یکبار مصرف.
        """
        if not request.user.is_authenticated:  # بررسی اینکه آیا کاربر وارد نشده است
            otp = get_object_or_404(OneTimePassword, token=token)  # دریافت رمز یکبار مصرف با توکن

            if otp:
            
                if otp.registration_otps:  # بررسی وجود ثبت‌نام مرتبط
                    serializer = UserRegisterSerializer(data=request.data, context={'otp_token': otp.token})  # سریالایزر ثبت‌نام

                    if serializer.is_valid(raise_exception=True):  # اعتبارسنجی داده‌ها

                        user_data = serializer.create(
                            validated_data=serializer.validated_data, 
                            token=token
                        )  # ذخیره کاربر

                        return Response({  # پاسخ موفق با جزئیات کاربر
                            'Detail': {
                                'Message': 'User created successfully',
                                'User': user_data['user'],
                                'Token': user_data['tokens']
                            }
                        }, status=status.HTTP_201_CREATED)

                    else:
                        return Response(
                            {'Detail': serializer.errors}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )  # پاسخ خطا
                else:
                    return Response(
                        {'Detail': 'Otp register does not exist.'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )  # پاسخ خطا اگر ثبت‌نام وجود ندارد
            else:
                return Response(
                    {'Detail': 'OTP does not exist'}, 
                    status=status.HTTP_404_NOT_FOUND
                )  # پاسخ خطا اگر رمز یافت نشود
        else:
            return Response(
                {'Detail': 'You are already authenticated'}, 
                status=status.HTTP_400_BAD_REQUEST
            )  # پاسخ خطا اگر کاربر قبلاً احراز هویت شده باشد
