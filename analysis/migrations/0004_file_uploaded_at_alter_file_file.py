# Generated by Django 4.2 on 2024-07-01 21:21

import analysis.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0003_rename_detail_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to=analysis.models.user_directory_path, verbose_name='CSV File'),
        ),
    ]
