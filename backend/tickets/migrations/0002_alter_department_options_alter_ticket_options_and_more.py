# Generated by Django 5.2 on 2025-04-03 13:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'ordering': ['name'], 'verbose_name': 'Dział', 'verbose_name_plural': 'Działy'},
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ['-created_at'], 'verbose_name': 'Zgłoszenie', 'verbose_name_plural': 'Zgłoszenia'},
        ),
        migrations.AddField(
            model_name='department',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Email kontaktowy'),
        ),
        migrations.AddField(
            model_name='department',
            name='description',
            field=models.TextField(blank=True, verbose_name='Opis'),
        ),
        migrations.AddField(
            model_name='department',
            name='identification',
            field=models.CharField(default=None, max_length=10, unique=True, verbose_name='ID działu'),
        ),
        migrations.AddField(
            model_name='department',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='assigned',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_tickets', to=settings.AUTH_USER_MODEL, verbose_name='Przypisane do'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='closed_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Zgłoszenie zamknięte'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='due',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Termin realizacji'),
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Nazwa działu'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='category',
            field=models.CharField(choices=[('HARDWARE_FAILURE', 'Problem ze sprzętem'), ('SOFTWARE_FAILURE', 'Problem z oprogramowaniem'), ('DEVICE_NEEDS', 'Zapotrzebowanie na sprzęt')], default=None, max_length=32, verbose_name='Ketegoria zgłoszenia'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Zgłaszający'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.TextField(verbose_name='Opis problemu'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='of_department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='tickets.department'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.CharField(choices=[('LOW', 'Niski'), ('MEDIUM', 'Średni'), ('HIGH', 'Wysoki'), ('URGENT', 'Najwyższy')], default='LOW', max_length=20, verbose_name='Priorytet zgłoszenia'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('OPEN', 'Otwarty'), ('IN_PROGRESS', 'W trakcie...'), ('CLOSED', 'Zamknięty')], default='OPEN', max_length=20, verbose_name='Status zgłoszenia'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Tytuł'),
        ),
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('position', models.CharField(max_length=100, verbose_name='Stanowisko')),
                ('is_department_manager', models.BooleanField(default=False)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tickets.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
