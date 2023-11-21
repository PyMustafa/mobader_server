# Generated by Django 4.2.7 on 2023-11-17 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobaderapp', '0029_bookdoctor_book_type_bookdoctor_is_paid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookdoctor',
            name='book_type',
            field=models.CharField(blank=True, choices=[('VISIT', 'Visit'), ('MEET', 'Meet')], default='VISIT', max_length=20),
        ),
    ]
