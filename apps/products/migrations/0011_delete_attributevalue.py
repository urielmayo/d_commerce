# Generated by Django 4.1.1 on 2023-01-26 03:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_attribute_value'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AttributeValue',
        ),
    ]
