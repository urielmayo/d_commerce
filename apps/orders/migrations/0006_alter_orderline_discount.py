# Generated by Django 4.1.1 on 2023-01-24 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_order_total_taxes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderline',
            name='discount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]