# Generated by Django 4.1.1 on 2023-01-22 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_shoppingcart_shoppingcartline'),
        ('orders', '0002_alter_order_customer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer_billing_address',
            field=models.ForeignKey(limit_choices_to={'type': 'billing'}, on_delete=django.db.models.deletion.DO_NOTHING, related_name='billing_address', to='users.profileaddress'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profilepayment'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_shipping_address',
            field=models.ForeignKey(limit_choices_to={'type': 'shipping'}, on_delete=django.db.models.deletion.DO_NOTHING, related_name='shipping_address', to='users.profileaddress'),
        ),
    ]
