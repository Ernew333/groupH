# Generated by Django 5.0.3 on 2024-04-30 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventories', '0007_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(default=None, upload_to='inventories/media/images'),
        ),
    ]
