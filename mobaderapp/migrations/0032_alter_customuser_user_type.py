# Generated by Django 4.2.7 on 2023-11-18 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobaderapp', '0031_eventslider_mediacenter_offer_teamslider_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[(1, 'Admin'), (2, 'Staff'), (3, 'Doctor'), (4, 'Nurse'), (5, 'Lap'), (6, 'Pharmacy'), (7, 'Physiotherapist'), (8, 'Patient')], default=8, max_length=2),
        ),
    ]
