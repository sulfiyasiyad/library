# Generated by Django 4.2.6 on 2024-03-16 02:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vookeys', '0013_rent_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('requestbook', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vookeys.requestbook')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]