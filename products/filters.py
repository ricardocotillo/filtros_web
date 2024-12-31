from django_filters import FilterSet
from django_filters.rest_framework import FilterSet as RestFilterSet
from utils.filters import NumberRangeFilter, NumberInFilter
from .models import Producto, Modelo, Marca


class ProductoFilterSet(FilterSet):
    class Meta:
        model = Producto
        fields = {
            'codigo': ('icontains', 'iexact',),
            'aplicaciones': ('iexact',),
            'equivalencias__codigo': ('icontains', 'iexact'),
        }


class ModeloRestFilterSet(RestFilterSet):
    class Meta:
        model = Modelo
        fields = {
            'nombre': ('iexact', 'icontains',)
        }


class MarcaRestFilterSet(RestFilterSet):
    class Meta:
        model = Marca
        fields = {
            'nombre': ('iexact', 'icontains',)
        }


class ProductoRestFilterSet(RestFilterSet):
    producto_modelos__ano__range = NumberRangeFilter(
        field_name='producto_modelos__ano',
        lookup_expr='range',
    )
    producto_modelos__modelo__marca__in = NumberInFilter(
        field_name='producto_modelos__modelo__marca',
        lookup_expr='in',
    )
    producto_modelos__modelo__in = NumberInFilter(
        field_name='producto_modelos__modelo',
        lookup_expr='in',
    )

    class Meta:
        model = Producto
        fields = {
            'codigo': ('icontains', 'iexact',),
            'aplicaciones': ('iexact', 'icontains',),
            'equivalencias__codigo': ('iexact',),
            'producto_modelos__ano': ('exact', 'range'),
            'producto_modelos__modelo': ('exact', 'in',),
            'producto_modelos__modelo__marca': ('exact', 'in')
        }
