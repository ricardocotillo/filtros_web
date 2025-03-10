# Generated by Django 5.1 on 2024-09-25 16:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=25)),
                ('linea', models.CharField(max_length=25)),
                ('tipo', models.CharField(max_length=25)),
                ('aplicaciones', models.TextField(blank=True)),
                ('diametro_exterior', models.CharField(blank=True, max_length=50)),
                ('diametro_interior', models.CharField(blank=True, max_length=50)),
                ('altura', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('pzs_x_caja', models.PositiveIntegerField(null=True)),
                ('valv_antidr', models.CharField(blank=True, choices=[('si', 'SI'), ('no', 'NO')], max_length=2)),
                ('valv_by_pass', models.CharField(blank=True, choices=[('si', 'SI'), ('no', 'NO')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Equivalence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('brand', models.CharField(max_length=25)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equivalences', to='products.product')),
            ],
        ),
    ]
