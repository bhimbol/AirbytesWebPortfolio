from django.contrib import admin
from .models import Product, Valuation, Promo, PromoProduct, Badstock, Undelivered, Count

#from .models import Invoice

#class InvoiceAdmin(admin.ModelAdmin):
#    list_display = ('number', 'date', 'amount', 'customer_number', 'customer_name', 'remarks',)
#    search_fields = ('number', 'customer_name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_sku', 'description', 'qtyperpcs', 'bccs', 'bcib', 'bcpcs',)
    search_fields = ('product_sku', 'description',)

class PromoAdmin(admin.ModelAdmin):
    list_display = ('promo_sku', 'mech_per_pcs',)
    search_fields = ('promo_sku',)

class PromoProductAdmin(admin.ModelAdmin):
    list_display = ('promo','product',)
    search_fields = ('product',)

@admin.register(Count)
class CountAdmin(admin.ModelAdmin):
    list_display = ('product_sku', 'cs', 'ib', 'pcs',)
    search_fields = ('product_sku',)

@admin.register(Valuation)
class ValuationAdmin(admin.ModelAdmin):
    list_display = ('product_sku', 'cs', 'ib', 'pcs',)
    search_fields = ('product_sku',)

@admin.register(Badstock)
class BadstockAdmin(admin.ModelAdmin):
    list_display = ('product_sku', 'cs', 'ib', 'pcs', 'remarks')
    search_fields = ('product_sku',)

@admin.register(Undelivered)
class UndeliveredAdmin(admin.ModelAdmin):
    list_display = ('product_sku', 'cs', 'ib', 'pcs',)
    search_fields = ('product_sku',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Promo, PromoAdmin)
admin.site.register(PromoProduct, PromoProductAdmin)
#admin.site.register(Invoice, InvoiceAdmin)

