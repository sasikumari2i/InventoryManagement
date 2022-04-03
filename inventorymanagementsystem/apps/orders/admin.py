from django.contrib import admin

# Register your models here.


from . models import Vendor, Order, Customer, OrderProduct

admin.site.register(Vendor)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(OrderProduct)