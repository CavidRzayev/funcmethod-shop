# Generated by Django 2.2.10 on 2020-07-07 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_auto_20200707_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companypromocode',
            name='count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Promocoddan istifade olunub'),
        ),
        migrations.AlterField(
            model_name='companypromocode',
            name='faiz',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Endirim Faiz Derecesi'),
        ),
        migrations.AlterField(
            model_name='companypromocode',
            name='limit',
            field=models.IntegerField(default=0, verbose_name='Maksimum istifade Dayi - Limit ( +1 yazilmalidi)'),
        ),
        migrations.AlterField(
            model_name='companypromocode',
            name='money',
            field=models.CharField(blank=True, default=0, max_length=300, null=True, verbose_name='Manat'),
        ),
    ]
