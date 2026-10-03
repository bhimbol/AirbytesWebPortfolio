from django.contrib import admin
from .models import Invoice

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'amount', 'customer_number', 'customer_name', 'remarks', 's_code',)
    search_fields = ('number', 'customer_name',)

admin.site.register(Invoice, InvoiceAdmin)
