# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-04 19:33
from __future__ import unicode_literals

from django.db import migrations, models
import workspace.models.models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0012_auto_20160504_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='path',
            field=models.FileField(upload_to=workspace.models.renomage),
        ),
    ]
