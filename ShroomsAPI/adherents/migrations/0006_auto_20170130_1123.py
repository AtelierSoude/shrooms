# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-30 10:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_auto_20170130_1123'),
        ('adherents', '0005_auto_20170130_1035'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdherentStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
            ],
            options={
                'verbose_name': "adherent's status",
                'verbose_name_plural': "adherents' statuses",
            },
        ),
        migrations.RemoveField(
            model_name='adherentgroup',
            name='basegroup_ptr',
        ),
        migrations.RemoveField(
            model_name='subscriptiontype',
            name='group',
        ),
        migrations.DeleteModel(
            name='AdherentGroup',
        ),
        migrations.AddField(
            model_name='subscriptiontype',
            name='status',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='adherents.AdherentStatus'),
            preserve_default=False,
        ),
    ]
