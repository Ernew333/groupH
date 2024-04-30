# Generated by Django 5.0.3 on 2024-04-30 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventories', '0006_remove_item_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(default=3, upload_to='inventories/media/images'),
            preserve_default=False,
        ),
    ]