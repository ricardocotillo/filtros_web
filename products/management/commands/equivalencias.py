import csv
from django.core.management.base import BaseCommand
from products.models import Equivalencia, Producto


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        f = open('equivalencias.csv')
        datos_reader = csv.reader(f)
        next(datos_reader)
        for e in datos_reader:
            producto = Producto.objects.filter(codigo=e[2].strip()).first()
            if producto:
                Equivalencia.objects.get_or_create(
                    codigo=e[0].strip(),
                    marca=e[1].strip(),
                    producto=producto,
                )
