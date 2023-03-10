# Generated by Django 4.1.1 on 2023-03-02 03:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtotal', models.FloatField()),
                ('total_taxes', models.FloatField(blank=True, null=True)),
                ('total', models.FloatField()),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('paid', 'Paid'), ('on_ship', 'On Ship'), ('shipped', 'Shipped'), ('cancelled', 'Cancelled')], default='draft', max_length=10)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField()),
                ('discount', models.FloatField(blank=True, null=True)),
                ('unit_price', models.FloatField()),
                ('line_total', models.FloatField()),
                ('status', models.CharField(choices=[('to_ship', 'To Ship'), ('in_transit', 'In Transit'), ('delivered', 'Delivered')], default='to_ship', max_length=30)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_lines', to='orders.order')),
            ],
            options={
                'verbose_name': 'Order Line',
                'verbose_name_plural': 'Order Lines',
            },
        ),
    ]
