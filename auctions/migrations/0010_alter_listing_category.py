# Generated by Django 4.0.6 on 2022-08-07 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_user_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='auctions.category'),
        ),
    ]
