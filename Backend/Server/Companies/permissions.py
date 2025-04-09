from rest_framework.permissions import BasePermission, SAFE_METHODS  # وارد کردن کلاس پایه‌ی دسترسی و متغیر SAFE_METHODS که شامل متدهای ایمن (مانند GET, HEAD, OPTIONS) می‌شود



class IsAdminOrOwnerForUpdateAndEmployerForCreate(BasePermission):
    """
    مجوز سفارشی برای موارد زیر:
    - تنها کاربران مدیرعامل (کاربران با نوع EM) می‌توانند شرکت ایجاد کنند.
    - تنها مدیران یا مالک شرکت (کاربر صاحب فیلد employer) امکان به‌روزرسانی شرکت را دارند.
    """

    def has_permission(self, request, view):
        # اجازه‌ی دسترسی به متدهای ایمن (مانند GET, HEAD, OPTIONS) برای همه کاربران داده می‌شود
        if request.method in SAFE_METHODS:
            return True

        # برای درخواست‌های CREATE (POST)، تنها کاربران احراز هویت‌شده با نوع کاربری 'EM' (کارفرما) مجاز به ایجاد شرکت هستند
        if request.method == 'POST':
            return request.user.is_authenticated and request.user.user_type == 'EM'

        # در موارد دیگر (برای مثال PUT، PATCH، DELETE) بررسی سطح دسترسی در سطح شیء انجام می‌شود
        return True

    def has_object_permission(self, request, view, obj):
        """
        دسترسی سطح شیء (Object-level permissions) برای به‌روزرسانی:
        - برای متدهای ایمن، مجوز صادر می‌شود.
        - برای به‌روزرسانی (به‌طور خاص متد PUT)، تنها مدیران یا مالک شرکت (کاربر موجود در فیلد employer) اجازه‌ی ویرایش دارند.
        """
        # اجازه‌ی دسترسی برای متدهای ایمن به همه داده می‌شود
        if request.method in SAFE_METHODS:
            return True

        # بررسی به‌روزرسانی (PUT)، فقط اگر کاربر احراز هویت شده باشد و یا از سطح دسترسی مدیر باشد یا همان مالک شرکت باشد
        if request.method in ('PUT',):  # در اینجا به‌طور خاص متد PUT بررسی می‌شود
            return request.user.is_authenticated and (
                request.user.is_admin or obj.employer == request.user
            )

        # سایر متدها (مانند DELETE یا PATCH) بسته به نیاز می‌توانند مجوز داده شوند؛ اما در اینجا به‌طور پیش‌فرض ممنوع هستند.
        return False
