# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urlyapp', '0005_auto_20150620_1542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='click',
            name='user',
        ),
        migrations.AddField(
            model_name='click',
            name='profile',
            field=models.ForeignKey(to='urlyapp.Profile', null=True),
        ),
    ]
