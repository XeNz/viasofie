# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-03 08:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0023_auto_20160502_1628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dealstatus',
            name='visible_to_user',
        ),
        migrations.AddField(
            model_name='status',
            name='visible_to_user',
            field=models.BooleanField(default=True),
        ),
    ]