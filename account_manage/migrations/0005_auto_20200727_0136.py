# Generated by Django 3.0.8 on 2020-07-27 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_manage', '0004_auto_20200726_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.PositiveIntegerField(default=1, null=True),
        ),
    ]