# Generated by Django 2.2.10 on 2020-06-01 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0031_auto_20200602_0050'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='month_12',
            field=models.DecimalField(blank=True, decimal_places=0, default=1, max_digits=9, verbose_name='Kredit 12 ay ucun ayliq odenis'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='month_15',
            field=models.DecimalField(blank=True, decimal_places=0, default=1, max_digits=9, verbose_name='Kredit 15 ay ucun ayliq odenis'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='month_18',
            field=models.DecimalField(blank=True, decimal_places=0, default=1, max_digits=9, verbose_name='Kredit 18 ay ucun ayliq odenis'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='month_6',
            field=models.DecimalField(blank=True, decimal_places=0, default=1, max_digits=9, verbose_name='Kredit 6 ay ucun ayliq odenis'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='month_9',
            field=models.DecimalField(blank=True, decimal_places=0, default=1, max_digits=9, verbose_name='Kredit 9 ay ucun ayliq odenis'),
            preserve_default=False,
        ),
    ]