# Generated by Django 2.2.10 on 2020-05-13 09:51

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20200510_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='code',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=ckeditor.fields.RichTextField(default=1),
            preserve_default=False,
        ),
    ]
