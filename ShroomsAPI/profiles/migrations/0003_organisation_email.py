# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-23 15:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20170123_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
