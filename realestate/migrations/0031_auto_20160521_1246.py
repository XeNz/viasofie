# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-21 10:46
from __future__ import unicode_literals

from django.db import migrations, models
import realestate.models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0030_auto_20160521_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='logo',
            field=models.ImageField(blank=True, upload_to=realestate.models.create_partner_images_path, validators=[realestate.models.Partner.validate_image]),
        ),
    ]
