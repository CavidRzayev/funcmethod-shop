# Generated by Django 2.2.10 on 2020-05-20 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_color_color_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='slug',
            field=models.SlugField(blank=True, max_length=200),
        ),
    ]