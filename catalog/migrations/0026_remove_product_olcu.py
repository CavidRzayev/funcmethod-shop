# Generated by Django 2.1.5 on 2020-04-16 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0025_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='olcu',
        ),
    ]