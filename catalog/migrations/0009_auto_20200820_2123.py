# Generated by Django 2.2 on 2020-08-20 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20200819_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landingpage',
            name='slug',
            field=models.SlugField(blank=True, max_length=500),
        ),
    ]
