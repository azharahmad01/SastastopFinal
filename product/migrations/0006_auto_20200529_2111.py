# Generated by Django 3.0.5 on 2020-05-29 21:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0005_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bagitem',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bag', to=settings.AUTH_USER_MODEL),
        ),
    ]
