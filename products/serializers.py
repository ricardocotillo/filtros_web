from rest_framework import serializers
from .models import Producto, Marca, Modelo, ProductoModelo


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'


class ModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = '__all__'


class ProductoModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoModelo
        fields = '__all__'
