from django.contrib import admin
from products.models import Product, Variation


class Variationinline(admin.TabularInline):
    model = Variation
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_description',
                    'get_price_marketing_formated', 'get_price_promotional_marketing_formated']
    inlines = [
        Variationinline
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation)
