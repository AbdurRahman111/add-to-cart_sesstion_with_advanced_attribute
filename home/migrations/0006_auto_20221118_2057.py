# Generated by Django 3.2 on 2022-11-18 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_delete_attribute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='embroidery',
            name='Additional_Price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='size',
            name='price',
            field=models.IntegerField(),
        ),
    ]
