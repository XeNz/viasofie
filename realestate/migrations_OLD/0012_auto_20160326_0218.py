# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-26 01:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0011_auto_20160322_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='description_text',
            field=models.TextField(),
        ),
    ]
