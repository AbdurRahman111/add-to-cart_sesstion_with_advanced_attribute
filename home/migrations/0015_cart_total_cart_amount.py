# Generated by Django 3.2 on 2022-11-19 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20221120_0207'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='Total_Cart_Amount',
            field=models.IntegerField(default=0),
        ),
    ]
