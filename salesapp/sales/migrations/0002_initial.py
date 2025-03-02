# Generated by Django 5.1.6 on 2025-02-27 18:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('sales', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='salesorder',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='products',
            field=models.ManyToManyField(through='sales.OrderItem', to='product.product'),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='sales_rep',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.salesorder'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sales.salesorder'),
        ),
    ]
