# Generated by Django 5.1.1 on 2024-10-22 01:22

import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_cartorder_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='full_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='oid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', blank=True, length=8, max_length=20, null=True, prefix=''),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='saved',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=12),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='shipping_method',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='sku',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', blank=True, length=5, max_length=20, null=True, prefix='SKU'),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='stripe_payment_intent',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='tracking_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='tracking_website_address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='price',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=12),
        ),
    ]
