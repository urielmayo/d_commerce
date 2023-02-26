# Generated by Django 4.1.1 on 2022-12-30 02:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Attribute',
                'verbose_name_plural': 'Attributes',
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'verbose_name': 'Product Category',
                'verbose_name_plural': 'Product Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('sku', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('description', models.TextField(blank=True)),
                ('stock_qty', models.PositiveIntegerField()),
                ('slug', models.SlugField()),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.brand')),
                ('categories', models.ManyToManyField(to='products.productcategory')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=50)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.attribute')),
            ],
            options={
                'verbose_name': 'Attribute Value',
                'verbose_name_plural': 'Attribute Values',
            },
        ),
        migrations.AddField(
            model_name='attribute',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
    ]