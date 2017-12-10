# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-05 15:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productproduct',
            name='sale_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_product', to='shop.SaleOrder'),
        ),
    ]