import csv
from django.core.management.base import BaseCommand
from products.models import Producto, Marca, Modelo, ProductoModelo


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        f = open('datos.csv')
        datos_reader = csv.reader(f)
        next(datos_reader)
        productos = {}
        marcas = {}
        modelos = {}
        datos = [row for row in datos_reader]
        # create marcas
        for d in datos:
            nombre = d[5].strip().lower().capitalize()
            if nombre and not marcas.get(nombre):
                marca, _ = Marca.objects.get_or_create(
                    nombre=nombre,
                )
                marcas[marca.nombre] = marca

        for d in datos:
            nombre = d[6].strip().lower().capitalize()
            marca_nombre = d[5].strip().lower().capitalize()
            if nombre and not modelos.get(nombre):
                marca: Marca = marcas[marca_nombre]
                modelo, _ = Modelo.objects.get_or_create(
                    nombre=nombre,
                    defaults={
                        'marca_id': marca.pk,
                    }
                )
                modelos[modelo.nombre] = modelo

        for d in datos:
            codigo = d[0].strip().upper()
            producto = productos.get(codigo)
            if not producto:
                producto, _ = Producto.objects.get_or_create(
                    codigo=codigo,
                    defaults={
                        'diametro_interior': d[1].strip(),
                        'diametro_exterior': d[2].strip(),
                        'altura': d[3].strip(),
                        'aplicaciones': d[4].strip(),
                        'tipo': d[8].strip(),
                        'descripcion': d[9].strip(),
                        'empaquetadura': d[10].strip(),
                        'valv_antidr': d[11].strip(),
                        'valv_by_pass': d[12].strip(),
                        'pzs_x_caja': d[13].strip(),
                    },
                )
            modelo_nombre = d[6].strip().lower().capitalize()
            if modelo_nombre:
                modelo = modelos[modelo_nombre]

                ProductoModelo.objects.get_or_create(
                    producto=producto,
                    modelo=modelo,
                    ano=int(d[7].strip())
                )
