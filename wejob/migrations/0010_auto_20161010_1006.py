# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-10 08:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wejob', '0009_auto_20161009_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annonce',
            name='published',
            field=models.DateField(default=datetime.datetime(2016, 10, 10, 10, 6, 42, 387636), verbose_name='Publi\xe9e'),
        ),
        migrations.AlterField(
            model_name='annonce',
            name='type_contrat',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='wejob.TypeContrat'),
        ),
    ]
