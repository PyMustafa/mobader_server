# Generated by Django 4.2.7 on 2023-11-14 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobaderapp', '0021_alter_patientuser_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientuser',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='patients/'),
        ),
    ]
