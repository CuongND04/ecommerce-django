# Generated by Django 5.1.1 on 2024-10-29 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_cartorder_coupons'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='vendor',
        ),
        migrations.DeleteModel(
            name='Vendor',
        ),
    ]
