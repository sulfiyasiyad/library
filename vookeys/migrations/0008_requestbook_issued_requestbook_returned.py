# Generated by Django 4.2.6 on 2024-03-11 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vookeys', '0007_requestbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestbook',
            name='issued',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='requestbook',
            name='returned',
            field=models.BooleanField(default=False),
        ),
    ]
