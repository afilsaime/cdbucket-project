# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-03 13:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0006_music_auteur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='auteur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
