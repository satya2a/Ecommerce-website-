from django.contrib import admin
from .models import Product, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "featured", "created_at")
    list_filter = ("category", "featured")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "price", "quantity", "subtotal")

    def subtotal(self, obj):
        return obj.subtotal


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "total_amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "email", "phone")
    inlines = [OrderItemInline]
    readonly_fields = ("total_amount", "created_at")
