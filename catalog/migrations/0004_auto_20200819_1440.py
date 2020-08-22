# Generated by Django 2.2.10 on 2020-08-19 14:40

from django.db import migrations
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20200819_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landingpage',
            name='products',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, to='catalog.Product'),
        ),
    ]