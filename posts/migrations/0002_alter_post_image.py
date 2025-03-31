# Generated by Django 5.1.7 on 2025-03-31 03:03

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=['middel', 'center'], force_format=None, keep_meta=True, quality=-1, scale=None, size=[500, 500], upload_to='image/%Y/%m'),
        ),
    ]
