# Generated by Django 4.1.1 on 2023-01-15 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributevalue',
            name='false_field',
            field=models.BooleanField(null=True),
        ),
    ]
