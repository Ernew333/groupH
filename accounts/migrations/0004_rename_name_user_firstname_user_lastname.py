# Generated by Django 5.0.4 on 2024-04-30 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_name_user_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='firstname',
        ),
        migrations.AddField(
            model_name='user',
            name='lastname',
            field=models.CharField(default=556, max_length=100),
            preserve_default=False,
        ),
    ]
