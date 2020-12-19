# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-11-07 12:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Orientador',
            fields=[
                ('cod_lattes_16', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'orientadores',
                'managed': False,
                'verbose_name_plural': 'Orientadores',
            },
        ),
        migrations.CreateModel(
            name='Programa',
            fields=[
                ('cod_capes', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'programas',
                'managed': False,
                'verbose_name_plural': 'Programas',
            },
        ),
        migrations.CreateModel(
            name='ProgramaOrientador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'programas_orientadores',
                'managed': False,
                'verbose_name_plural': 'Programas/Orientadores',
            },
        ),
    ]
