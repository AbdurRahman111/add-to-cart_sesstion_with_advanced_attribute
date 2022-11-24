# Generated by Django 3.2 on 2022-11-18 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20221118_2057'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, max_length=300, null=True)),
                ('device_id', models.CharField(blank=True, max_length=300, null=True)),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('Color', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='home.color')),
                ('Embroidery', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='home.embroidery')),
                ('Size', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='home.size')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product_table')),
            ],
            options={
                'verbose_name_plural': 'CartItems',
            },
        ),
    ]