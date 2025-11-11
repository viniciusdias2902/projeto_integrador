from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Driver


class DriverModelAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "shift", "role", "dailyPaymentCents", "get_email")
    list_filter = ("shift", "role")
    search_fields = ("name", "phone", "user__email")
    readonly_fields = ("role",)

    fieldsets = (
        ("Personal Information", {"fields": ("name", "phone")}),
        ("Work Information", {"fields": ("shift", "dailyPaymentCents")}),
        ("Account Information", {"fields": ("user", "role")}),
    )

    def get_email(self, obj):
        return obj.user.email if obj.user else "-"

    get_email.short_description = "Email"
    get_email.admin_order_field = "user__email"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.user:
            group, _ = Group.objects.get_or_create(name="drivers")
            obj.user.groups.add(group)


admin.site.register(Driver, DriverModelAdmin)
