# Generated by Django 4.2.7 on 2023-11-14 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobaderapp', '0020_imagegallery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientuser',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='patients/%Y/%m/%d/'),
        ),
    ]