# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-30 10:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20170130_1040'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grouprole',
            options={'verbose_name': 'role', 'verbose_name_plural': 'roles'},
        ),
        migrations.AlterField(
            model_name='grouprole',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rôles', to='profiles.BaseGroup', verbose_name='group'),
        ),
    ]
