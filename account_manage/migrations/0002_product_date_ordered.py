# Generated by Django 3.0.8 on 2020-07-23 14:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account_manage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='date_ordered',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
