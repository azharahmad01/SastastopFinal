# Generated by Django 3.0.5 on 2020-07-10 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_auto_20200623_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdetail',
            name='color',
            field=models.CharField(choices=[('Blue', 'Blue'), ('Black', 'Black'), ('White', 'White'), ('Orange', 'Orange'), ('Green', 'Green'), ('Yellow', 'Yellow'), ('Grey', 'Grey'), ('Red', 'Red')], default='White', max_length=10),
        ),
    ]
