from django.contrib import admin
from .models import Producto, Marca, Modelo


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'tipo',)
    search_fields = ('codigo',)


admin.site.register(Producto, ProductoAdmin)
admin.site.register(Marca)
admin.site.register(Modelo)
