from rest_framework import permissions  # وارد کردن ماژول permissions از Django REST Framework

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    پرمیشن سفارشی:
    دسترسی خواندنی (read-only) را برای همه کاربران فراهم می‌کند،
    اما اجازه‌ی انجام عملیات نوشتاری (create, update, delete) فقط به کاربران ادمین (is_staff) داده می‌شود.
    """
    message = "Only admin users are allowed to create, update, or delete data."  
    # این پیام در صورت عدم مجوز ارسال می‌شود.

    def has_permission(self, request, view):
        # در صورتی که درخواست از نوع متدهای ایمن (GET, HEAD, OPTIONS) باشد،
        # اجازه دسترسی بدون در نظر گرفتن سطح کاربری داده می‌شود.
        if request.method in permissions.SAFE_METHODS:
            return True

        # در غیر این صورت (یعنی عملیات نوشتاری)، بررسی می‌شود که آیا کاربر وجود دارد و آیا کاربر ادمین (is_staff) است یا خیر.
        # تنها ادمین می‌توانند عملیات نوشتاری انجام دهند.
        return request.user and request.user.is_staff
