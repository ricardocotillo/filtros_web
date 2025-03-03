# Generated by Django 5.1 on 2024-09-25 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='altura',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='pzs_x_caja',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
