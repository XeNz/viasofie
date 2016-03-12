# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-08 01:17
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title_text', models.CharField(max_length=200)),
                ('description_text', models.CharField(max_length=200)),
                ('adress_text', models.CharField(max_length=200)),
                ('mailbox', models.CharField(max_length=200)),
                ('bedrooms', models.IntegerField(default=0)),
                ('bathrooms', models.IntegerField(default=0)),
                ('toilets', models.IntegerField(default=0)),
                ('gardens', models.IntegerField(default=0)),
                ('terraces', models.IntegerField(default=0)),
                ('sellingprice', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('constructiondate', models.DateField()),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
    ]
