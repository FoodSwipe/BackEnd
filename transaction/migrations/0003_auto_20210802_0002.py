# Generated by Django 3.1.4 on 2021-08-02 00:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transaction', '0002_auto_20210801_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='created_by',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='TransactionCreator', to=settings.AUTH_USER_MODEL),
        ),
    ]
