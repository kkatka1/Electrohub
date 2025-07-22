from django.contrib import admin
from django.db.models import F
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import messages
from rest_framework.exceptions import ValidationError

from .models import Contact, NetworkPoint, Product


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "country", "city", "street", "house_number")
    list_filter = ("city",)
    search_fields = ("email", "city")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "release_date")
    list_filter = ("release_date",)
    search_fields = ("name", "model")


@admin.register(NetworkPoint)
class NetworkPointAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "level",
        "supplier_link",
        "debt",
        "city",
        "created_at",
    )

    list_filter = ("level", "contacts__city")
    search_fields = ("name", "contacts__city")

    actions = ["clear_debt"]

    def supplier_link(self, obj):
        """Отображение ссылки на поставщика"""
        if obj.supplier:
            url = reverse("admin:network_networkpoint_change", args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "-"

    supplier_link.short_description = "Поставщик"
    supplier_link.admin_order_field = "supplier"

    def city(self, obj):
        """Город (отображение из связанной модели Contact)"""
        if obj.contacts and obj.contacts.city:
            return obj.contacts.city
        return "-"

    city.short_description = "Город"

    @admin.action(description="Очистить задолженность")
    def clear_debt(self, request, queryset):
        """Очистка задолженности для выбранных объектов"""
        updated = queryset.update(debt=F("debt") - F("debt"))
        self.message_user(request, f"Очищена задолженность для {updated} объектов")

    fieldsets = (
        ("Основная информация", {"fields": ("name", "level", "supplier", "debt")}),
        ("Контакты", {"fields": ("contacts",)}),
        ("Продукты", {"fields": ("products",)}),
    )

    readonly_fields = ("created_at",)
    filter_horizontal = ("products",)

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            messages.error(request, f"Ошибка: {str(e)}")
