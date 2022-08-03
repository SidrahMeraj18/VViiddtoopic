# Generated by Django 3.2 on 2022-05-25 08:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('srtgen', '0005_srtgen_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='srtgen',
            name='preview',
            field=models.FileField(blank=True, null=True, upload_to='previews_uploaded', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])]),
        ),
    ]