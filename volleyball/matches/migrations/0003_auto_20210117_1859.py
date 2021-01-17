# Generated by Django 3.1.5 on 2021-01-17 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matches', '0002_matchseat_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchseat',
            name='lock_expiration',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='matchseat',
            name='locked_for',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seat_locks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='matchseat',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seats', to=settings.AUTH_USER_MODEL),
        ),
    ]