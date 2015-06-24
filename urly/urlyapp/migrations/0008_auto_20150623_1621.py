# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urlyapp', '0007_bookmark_timestamp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookmark',
            old_name='url',
            new_name='_url',
        ),
    ]
