# Generated by Django 4.2.6 on 2024-04-07 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vookeys', '0027_lost_subtotal'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuebook',
            name='diff',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='issuebook',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
