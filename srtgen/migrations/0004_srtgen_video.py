# Generated by Django 3.2 on 2022-05-22 20:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('srtgen', '0003_srtgen_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='srtgen',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos_uploaded', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])]),
        ),
    ]