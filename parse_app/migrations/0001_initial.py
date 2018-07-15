# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-07-15 12:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('date', models.DateField()),
                ('open', models.FloatField(default=0)),
                ('higt', models.FloatField(default=0)),
                ('low', models.FloatField(default=0)),
                ('close', models.FloatField(default=0)),
                ('volume', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'parse_app_share',
            },
        ),
        migrations.CreateModel(
            name='Trader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('share', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('relation', models.CharField(max_length=32)),
                ('lastdate', models.DateField()),
                ('transaction_type', models.CharField(max_length=32)),
                ('owner_type', models.CharField(max_length=32)),
                ('shares_traded', models.IntegerField()),
                ('last_price', models.FloatField()),
                ('shares_held', models.IntegerField()),
            ],
            options={
                'db_table': 'parse_app_trader',
            },
        ),
    ]
