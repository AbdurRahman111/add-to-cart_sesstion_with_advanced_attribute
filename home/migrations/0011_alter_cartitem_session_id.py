# Generated by Django 3.2 on 2022-11-19 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20221120_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='session_id',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
