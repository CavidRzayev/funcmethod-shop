# Generated by Django 2.2.10 on 2020-05-20 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_auto_20200520_2156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='color',
            name='slug',
        ),
        migrations.AlterField(
            model_name='color',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color', to='catalog.Product'),
        ),
    ]
