from django.contrib import admin

from ..orders.models import Order
from ..orders.serializers import OrderSerializer
from .models import Invoice, Payment


# Register your models here.


class OrderInline(admin.TabularInline):
    model = Order
    extra = 1


class InvoiceAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Invoice Details",
            {
                "fields": [
                    "amount",
                    "created_date",
                    "payment_deadline",
                    "payment_status",
                ]
            },
        ),
    ]
    inlines = [OrderInline]
    serializer_class = OrderSerializer(read_only=True)


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Payment)
