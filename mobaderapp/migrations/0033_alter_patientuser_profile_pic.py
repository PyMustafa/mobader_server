# Generated by Django 4.2.7 on 2023-11-18 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobaderapp', '0032_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientuser',
            name='profile_pic',
            field=models.FileField(default='', upload_to=''),
        ),
    ]
