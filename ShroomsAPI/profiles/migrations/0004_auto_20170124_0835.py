# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-24 07:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_organisation_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shroom',
            name='organisation_ptr',
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'user profile', 'verbose_name_plural': 'user profiles'},
        ),
        migrations.DeleteModel(
            name='Shroom',
        ),
    ]
