from django.contrib import admin
from order.models import Order, OrderItem


class ItemOrderInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [ItemOrderInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
