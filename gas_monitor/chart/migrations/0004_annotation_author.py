# Generated by Django 5.2.1 on 2025-05-14 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0003_gasrecord_gas_rate_v1_gasrecord_gas_rate_v2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='author',
            field=models.CharField(blank=True, max_length=100, verbose_name='Автор'),
        ),
    ]
