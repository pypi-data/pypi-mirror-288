from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import LoginAuditEvent, RequestAuditEvent
from .settings import DRF_AUDIT_TRAIL_USER_PK_NAME

UserModel = get_user_model()


def _get_user_by_id(user_id: str | None):
    try:
        filter_param = {DRF_AUDIT_TRAIL_USER_PK_NAME: user_id}
        user = UserModel.objects.filter(**filter_param).first()
        if user is not None:
            return user
    except ValueError:
        pass


class RequestAuditEventModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "method",
        "url",
        "status_code",
        "_user",
        "datetime",
        "request_type",
    )
    list_filter = ("method", "ip_addresses")
    search_fields = ("method", "ip_addresses", "status_code")

    def _user(self, obj: RequestAuditEvent):
        return _get_user_by_id(obj.user)


admin.site.register(RequestAuditEvent, RequestAuditEventModelAdmin)


class LoginAuditEventModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "datetime",
        "request_ip_addresses",
        "request__status_code",
    )
    list_filter = ("status",)

    @admin.display()
    def request_ip_addresses(self, obj):
        if obj.request is not None:
            return obj.request.ip_addresses

    @admin.display()
    def request__status_code(self, obj):
        if obj.request is not None:
            return obj.request.status_code

    def user(self, obj):
        if obj.request is not None:
            return _get_user_by_id(obj.request.user)


admin.site.register(LoginAuditEvent, LoginAuditEventModelAdmin)
