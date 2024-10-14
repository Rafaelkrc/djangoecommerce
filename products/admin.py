from django.contrib import admin
from products.models import Product, Variation


class Variationinline(admin.TabularInline):
    model = Variation
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        Variationinline
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation)
