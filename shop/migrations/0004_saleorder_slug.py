# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-07 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_saleorder_date_reserve'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleorder',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True),
        ),
    ]
