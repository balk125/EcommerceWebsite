
from django.contrib import admin

# Register your models here.
from .models import product,Contact,orders,orderUpdate
class view_id(admin.ModelAdmin):
    readonly_fields = ('order_id',)



admin.site.register(orders,view_id)
admin.site.register(product)
admin.site.register(Contact)
admin.site.register(orderUpdate)
    