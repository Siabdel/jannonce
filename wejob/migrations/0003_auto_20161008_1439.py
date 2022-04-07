# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-08 12:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wejob', '0002_auto_20161008_1416'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeContrat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
            ],
        ),
        migrations.AlterField(
            model_name='annonce',
            name='published',
            field=models.DateField(default=datetime.datetime(2016, 10, 8, 14, 39, 41, 822682), verbose_name='Publi\xe9e'),
        ),
        migrations.AlterField(
            model_name='annonce',
            name='reponse_employeur',
            field=models.TextField(blank=True, null=True, verbose_name='R\xe9po    nse employeur'),
        ),
        migrations.AlterField(
            model_name='annonce',
            name='type_contrat',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='wejob.TypeContrat'),
            preserve_default=False,
        ),
    ]
