# Generated by Django 4.1.1 on 2023-01-03 01:16

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_numbwe_profileaddress_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profilepayment',
            name='type',
        ),
        migrations.AlterField(
            model_name='profilepayment',
            name='card_expiration_date',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='profilepayment',
            name='card_number',
            field=models.CharField(max_length=16, unique=True, validators=[users.models.only_numbers]),
        ),
    ]
