# Generated by Django 4.2.7 on 2023-11-15 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobaderapp', '0028_alter_adminuser_id_alter_customuser_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookdoctor',
            name='book_type',
            field=models.CharField(default='visit', max_length=20),
        ),
        migrations.AddField(
            model_name='bookdoctor',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bookdoctor',
            name='meeting_room',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
