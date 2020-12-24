# Generated by Django 3.1.3 on 2020-12-24 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_location', models.CharField(max_length=512)),
                ('custom_contact', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('custom_email', models.EmailField(max_length=254, null=True)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=8)),
                ('delivery_started', models.BooleanField(default=False)),
                ('delivery_started_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('is_delivered', models.BooleanField(default=False, editable=False)),
                ('delivery_charge', models.PositiveIntegerField(default=0)),
                ('loyalty_discount', models.PositiveBigIntegerField(default=0, editable=False)),
                ('grand_total', models.PositiveBigIntegerField(default=0, editable=False)),
                ('done_from_customer', models.BooleanField(default=False)),
                ('total_items', models.PositiveBigIntegerField(default=0, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment_type', models.CharField(choices=[('Cash', 'Cash')], default='Cash', max_length=20)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='OrderCreator', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='OrderUpdater', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='CartItemCreator', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='CartItem', to='item.menuitem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='cart.order')),
            ],
            options={
                'verbose_name': 'Cart Item',
                'verbose_name_plural': 'Cart Items',
                'unique_together': {('order', 'item')},
            },
        ),
    ]
