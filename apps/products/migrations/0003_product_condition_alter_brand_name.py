# Generated by Django 4.1.1 on 2023-03-05 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='condition',
            field=models.CharField(choices=[('new', 'New'), ('used', 'Used'), ('refurbished', 'Refurbished')], default='new', max_length=15),
        ),
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
