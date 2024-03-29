# Generated by Django 3.1.2 on 2020-12-17 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_product_discount_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pattern', models.CharField(max_length=30)),
                ('min_total_required', models.IntegerField()),
                ('expiry', models.DateTimeField()),
                ('is_percentage', models.BooleanField(default=True)),
                ('amount', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.coupon'),
        ),
    ]
