# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-03 14:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0007_auto_20160503_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='titre',
            field=models.CharField(choices=[('AL', 'Album'), ('PL', 'Playlist'), ('SI', 'Single')], default='AL', max_length=2),
        ),
    ]