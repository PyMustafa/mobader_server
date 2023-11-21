# Generated by Django 4.2.6 on 2023-11-07 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mobaderapp', '0009_booknurse'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookPhysio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(blank=True, choices=[('PEN', 'Pending'), ('ACC', 'Accepted'), ('REF', 'Refused')], default='PEN', max_length=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_physio', to='mobaderapp.patientuser')),
                ('physio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='physio_info', to='mobaderapp.physiotherapistuser')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_service_physio', to='mobaderapp.physiotherapistservice')),
                ('time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_time_physio_service', to='mobaderapp.physiotherapistservicetimes')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
