# Generated by Django 5.2.3 on 2025-07-18 12:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_alter_saleitem_cor_logo_1_alter_saleitem_cor_logo_2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='sale_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data da Venda'),
        ),
    ]
