# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-14 12:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import workspace.models.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('date_publication', models.DateField()),
                ('type_album', models.CharField(choices=[('AL', 'Album'), ('PL', 'Playlist'), ('SI', 'Single')], default='AL', max_length=2)),
                ('artiste', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('duree', models.DurationField()),
                ('active', models.BooleanField(default=True)),
                ('path', models.FileField(upload_to=workspace.models.renomage)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspace.Album')),
                ('auteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Signalement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('traite', models.BooleanField(default=False)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('artiste', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('music', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspace.Music')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intitule', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='music',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspace.Tag'),
        ),
        
    ]
