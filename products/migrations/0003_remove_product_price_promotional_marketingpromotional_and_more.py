# Generated by Django 5.1.2 on 2024-10-16 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_variation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price_promotional_marketingpromotional',
        ),
        migrations.AddField(
            model_name='product',
            name='price_promotional_marketing',
            field=models.FloatField(default=0, verbose_name='Price Prom.'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_marketing',
            field=models.FloatField(verbose_name='Price'),
        ),
    ]