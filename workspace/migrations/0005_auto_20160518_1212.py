# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-18 12:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0004_auto_20160518_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='email',
            field=models.EmailField(max_length=100, null=True),
        ),
    ]