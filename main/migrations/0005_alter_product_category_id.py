# Generated by Django 5.2.4 on 2025-07-22 21:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_product_category_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.category', verbose_name='related category'),
        ),
    ]
