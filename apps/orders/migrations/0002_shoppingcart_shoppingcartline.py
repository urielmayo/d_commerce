# Generated by Django 4.1.1 on 2023-01-14 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_product_price'),
        ('users', '0004_profileaddress_notes_profileaddress_state_and_more'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to='users.profile')),
            ],
            options={
                'verbose_name': 'Shopping Cart',
                'verbose_name_plural': 'Shopping Carts',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCartLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('shpping_cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart_lines', to='orders.shoppingcart')),
            ],
            options={
                'verbose_name': 'Shopping Cart Line',
                'verbose_name_plural': 'Shopping Cart Lines',
            },
        ),
    ]
