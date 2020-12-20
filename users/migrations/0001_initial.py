# Generated by Django 3.0.5 on 2020-05-24 13:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address1', models.CharField(max_length=100)),
                ('address2', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=6)),
                ('city', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=10)),
                ('users', models.ManyToManyField(related_name='addresses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]