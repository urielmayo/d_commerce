# Generated by Django 4.1.1 on 2023-01-15 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_attributevalue_false_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attributevalue',
            name='false_field',
        ),
    ]
