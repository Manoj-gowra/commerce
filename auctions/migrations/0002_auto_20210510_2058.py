# Generated by Django 3.1.7 on 2021-05-10 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='image_url',
            field=models.URLField(blank=True),
        ),
    ]