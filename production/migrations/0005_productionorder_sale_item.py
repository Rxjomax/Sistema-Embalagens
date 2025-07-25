# Generated by Django 5.2.3 on 2025-07-16 12:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0004_productionorder_sale'),
        ('sales', '0005_alter_saleitem_cor_logo_1_alter_saleitem_cor_logo_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='productionorder',
            name='sale_item',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='production_order', to='sales.saleitem', verbose_name='Item da Venda de Origem'),
        ),
    ]
