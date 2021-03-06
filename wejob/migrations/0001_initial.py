# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-07 08:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annonce',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100, verbose_name='Titre')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('lieu', models.CharField(blank=True, max_length=100, null=True)),
                ('salaire', models.BigIntegerField(blank=True, null=True, verbose_name='Salaire')),
                ('type_contrat', models.PositiveIntegerField(blank=True, choices=[(1, 'CDD'), (2, 'CDI'), (3, 'INTERIM'), (4, 'CONTRAT PRO'), (3, 'CONTRAT')], default=1, null=True, verbose_name='Type de contrat')),
                ('divers', models.CharField(blank=True, max_length=100, null=True, verbose_name='Divers')),
                ('formation', models.CharField(blank=True, max_length=100, null=True, verbose_name='Formation')),
                ('connaisannces', models.CharField(blank=True, max_length=500, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Cr\xe9er')),
                ('modified', models.DateField(auto_now=True, verbose_name='Modifi\xe9e')),
                ('reponse_employeur', models.TextField(blank=True, null=True, verbose_name='R\xe9ponse employeur')),
            ],
        ),
        migrations.CreateModel(
            name='Piece',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=100)),
                ('piece', models.FileField(upload_to='site_media/upload/')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Tache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('annonce', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wejob.Annonce')),
            ],
        ),
    ]
