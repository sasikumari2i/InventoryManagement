from django.contrib import admin

# Register your models here.
from .models import Vendor, Order, Customer, OrderProduct


admin.site.site_header = "Inventory Admin"
admin.site.site_title = "Inventory Admin Area"
admin.site.index_title = "Welcome to the Admin Page"


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Order Details",
            {
                "fields": [
                    "is_sales_order",
                    "order_date",
                    "delivery_date",
                    "vendors",
                    "customers",
                ]
            },
        ),
    ]
    inlines = [OrderProductInline]
    # serializer_class = OrderSerializer


admin.site.register(Order, OrderAdmin)
admin.site.register(Vendor)
# admin.site.register(Order)
admin.site.register(Customer)
# admin.site.register(OrderProduct)
