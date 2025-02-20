from django_filters import FilterSet, CharFilter
from django_filters.rest_framework import FilterSet as RestFilterSet
from django.db import models
from utils.filters import NumberRangeFilter, NumberInFilter, CharInFilter
from .models import Producto, Modelo, Marca


class ProductoFilterSet(FilterSet):
    class Meta:
        model = Producto
        fields = {
            'codigo': ('icontains', 'iexact',),
            'codigo_alt': ('icontains', 'iexact'),
            'aplicaciones': ('iexact',),
            'equivalencias__codigo': ('icontains', 'iexact'),
            'equivalencias__codigo_alt': ('icontains', 'iexact'),
        }
        filter_overrides = {
            models.GeneratedField: {
                'filter_class': CharFilter,
                'extra': lambda f: {'lookup_expr': 'icontains'},
            },
        }


class ModeloRestFilterSet(RestFilterSet):
    modelo_productos__ano__range = NumberRangeFilter(
        field_name='modelo_productos__ano',
        lookup_expr='range',
    )

    marca__in = NumberInFilter(
        field_name='marca',
        lookup_expr='in',
    )

    class Meta:
        model = Modelo
        fields = {
            'nombre': ('iexact', 'icontains',),
            'ano': ('exact', 'range',),
            'marca': ('exact', 'in'),
        }


class MarcaRestFilterSet(RestFilterSet):
    modelos__modelo_productos__ano__range = NumberRangeFilter(
        field_name='modelos__modelo_productos_ano',
        lookup_expr='range',
    )
    modelos__in = NumberInFilter(
        field_name='modelos',
        lookup_expr='in',
    )

    class Meta:
        model = Marca
        fields = {
            'nombre': ('iexact', 'icontains',),
            'modelos__modelo_productos__ano': ('exact', 'range',),
            'modelos': ('exact', 'in'),
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
    tipo__in = CharInFilter(
        field_name='tipo',
        lookup_expr='in',
    )

    class Meta:
        model = Producto
        fields = {
            'codigo': ('icontains', 'iexact',),
            'codigo_alt': ('icontains', 'iexact'),
            'aplicaciones': ('iexact', 'icontains',),
            'equivalencias__codigo': ('iexact', 'icontains'),
            'equivalencias__codigo_alt': ('iexact', 'icontains'),
            'producto_modelos__ano': ('exact', 'range'),
            'producto_modelos__modelo': ('exact', 'in',),
            'producto_modelos__modelo__marca': ('exact', 'in'),
            'tipo': ('exact', 'in'),
        }
        filter_overrides = {
            models.GeneratedField: {
                'filter_class': CharFilter,
                'extra': lambda f: {'lookup_expr': 'icontains'},
            },
        }
