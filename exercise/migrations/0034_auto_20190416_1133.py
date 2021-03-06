# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-04-16 08:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0033_auto_20190327_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.CharField(choices=[('error', 'Error'), ('initialized', 'Initialized'), ('ready', 'Ready'), ('rejected', 'Rejected'), ('unofficial', 'No effect on grading'), ('waiting', 'In grading')], default='initialized', max_length=32),
        ),
    ]
