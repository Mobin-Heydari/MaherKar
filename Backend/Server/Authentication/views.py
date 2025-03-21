from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError

from Users.models import User

from .serializers import LoginSerializer




# تعریف یک ویو کلاس‌بیس برای مدیریت ورود کاربران
class LoginAPIView(APIView):
    """
    ویو ورود برای احراز هویت کاربران و بازگرداندن توکن JWT.
    """
    
    # تعریف متد POST برای مدیریت درخواست‌های ورود
    def post(self, request):
        """
        مدیریت درخواست‌های POST برای ویو ورود.
        
        :param request: شیء درخواست دریافتی
        :return: شیء پاسخ با توکن‌های refresh و access
        """
        
        # ایجاد یک نمونه از سریالایزر با داده‌های درخواست
        serializer = LoginSerializer(data=request.data)

        # بررسی اینکه آیا کاربر قبلاً وارد شده است
        if request.user.is_authenticated:
            return Response({"message": "شما قبلاً وارد شده‌اید"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # بررسی اعتبار سریالایزر
            if serializer.is_valid():
                # استخراج شماره تلفن از داده‌های اعتبارسنجی شده
                phone = serializer.validated_data['phone']
                
                # دریافت شیء کاربر از دیتابیس
                user = User.objects.get(phone=phone)

                # بررسی اینکه آیا کاربر فعال است
                if not user.is_active:
                    # بازگشت یک پاسخ خطا در صورت غیرفعال بودن کاربر
                    return Response({'error': 'کاربر فعال نیست'}, status=status.HTTP_401_UNAUTHORIZED)
                
                # ایجاد یک توکن refresh برای کاربر
                refresh = RefreshToken.for_user(user)
                
                # بازگشت یک پاسخ با توکن‌های refresh و access
                return Response(
                    {
                        'refresh': str(refresh), 
                        'access': str(refresh.access_token)
                    },
                    status=status.HTTP_200_OK
                )
            else:
                # بازگشت یک پاسخ خطا با خطاهای سریالایزر
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # تعریف یک متد برای مدیریت استثناهایی که در طول اجرای ویو رخ می‌دهند
    def handle_exception(self, exc):
        """
        مدیریت استثناهایی که در طول اجرای ویو رخ می‌دهند.
        
        :param exc: شیء استثنا
        :return: شیء پاسخ با پیام خطا
        """
        
        # بررسی اینکه آیا استثنا خطای اعتبارسنجی است
        if isinstance(exc, ValidationError):
            # بازگشت یک پاسخ با پیام خطای اعتبارسنجی
            return Response({'error': 'خطای اعتبارسنجی'}, status=status.HTTP_400_BAD_REQUEST)
        # فراخوانی متد handle_exception کلاس والد برای سایر استثناها
        return super().handle_exception(exc)
