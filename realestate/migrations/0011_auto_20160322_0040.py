# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-21 23:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0010_auto_20160321_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='characteristics_property',
            name='characteristic_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristickey', to='realestate.Characteristic'),
        ),
    ]