# Generated by Django 2.0.3 on 2018-03-17 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('menus', '0001_initial'),
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='item',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='restaurants.Restaurant'),
        ),
    ]
