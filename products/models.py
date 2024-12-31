from django.db import models
from wagtail.admin.panels.field_panel import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Marca(models.Model):
    nombre = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.nombre


@register_snippet
class Modelo(models.Model):
    nombre = models.CharField(max_length=25, unique=True)
    marca = models.ForeignKey(
        Marca,
        on_delete=models.CASCADE,
        related_name='modelos',
    )

    def __str__(self):
        return self.nombre


@register_snippet
class Producto(models.Model):
    class Valv(models.TextChoices):
        SI = 'si', 'SI'
        NO = 'no', 'NO'
    codigo = models.CharField(max_length=25, unique=True)
    linea = models.CharField(max_length=25, blank=True)
    tipo = models.CharField(max_length=50, blank=True)
    modelos = models.ManyToManyField(
        Modelo,
        through='ProductoModelo',
        related_name='productos',
    )
    aplicaciones = models.TextField(blank=True)
    diametro_exterior = models.CharField(max_length=50, blank=True)
    diametro_interior = models.CharField(max_length=50, blank=True)
    altura = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )
    pzs_x_caja = models.PositiveIntegerField(null=True, blank=True)
    valv_antidr = models.CharField(
        max_length=2,
        choices=Valv.choices,
        blank=True,
    )
    valv_by_pass = models.CharField(
        max_length=2,
        choices=Valv.choices,
        blank=True,
    )
    descripcion = models.TextField(blank=True)
    empaquetadura = models.CharField(max_length=25, blank=True)
    destacado = models.BooleanField(default=False)
    promocion = models.BooleanField(default=False, verbose_name='Promoción')

    panels = [
        FieldPanel('codigo'),
        FieldPanel('linea'),
        FieldPanel('tipo'),
        FieldPanel('aplicaciones'),
        FieldPanel('diametro_exterior'),
        FieldPanel('diametro_interior'),
        FieldPanel('altura'),
        FieldPanel('pzs_x_caja', attrs={'required': False}),
        FieldPanel('valv_antidr'),
        FieldPanel('valv_by_pass'),
        FieldPanel('destacado'),
        FieldPanel('promocion'),
    ]

    def __str__(self) -> str:
        return self.codigo

    def save(self, *args, **kwargs) -> None:
        if not self.pzs_x_caja:
            self.pzs_x_caja = None
        if not self.altura:
            self.altura = None
        return super().save(*args, **kwargs)


@register_snippet
class ProductoModelo(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='producto_modelos',
    )
    modelo = models.ForeignKey(
        Modelo,
        on_delete=models.CASCADE,
        related_name='modelo_productos',
    )
    ano = models.PositiveIntegerField(verbose_name='año')

    def __str__(self):
        return (
            f'{self.producto.codigo} - {self.modelo.marca.nombre} - '
            f'{self.modelo.nombre} - {self.ano}'
        )


@register_snippet
class Equivalencia(models.Model):
    codigo = models.CharField(max_length=50)
    marca = models.CharField(max_length=25)
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='equivalencias',
    )

    panels = [
        FieldPanel('codigo'),
        FieldPanel('marca'),
        FieldPanel('producto'),
    ]

    def __str__(self) -> str:
        return f'{self.marca} - {self.codigo}'

    class Meta:
        unique_together = ('codigo', 'marca', 'producto')
