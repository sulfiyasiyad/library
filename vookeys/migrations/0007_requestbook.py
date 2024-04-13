# Generated by Django 4.2.6 on 2024-03-10 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vookeys', '0006_rent_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requestbook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Issuedate', models.DateField(blank=True, null=True)),
                ('returndate', models.DateField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vookeys.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]