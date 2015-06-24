# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urlyapp', '0006_auto_20150620_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
