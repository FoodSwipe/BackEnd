# Generated by Django 3.1.4 on 2020-12-26 00:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_mode', models.CharField(choices=[('create', 'Create'), ('update', 'Update'), ('delete', 'Delete'), ('start', 'Delivery Started'), ('complete', 'Delivery Completed')], default='Cash', editable=False, max_length=8)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('detail', models.CharField(max_length=512)),
                ('actor', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]