# Generated by Django 5.2 on 2025-04-04 17:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_alter_ticket_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='of_department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='tickets.department', verbose_name='Dział zgłaszający'),
        ),
    ]
