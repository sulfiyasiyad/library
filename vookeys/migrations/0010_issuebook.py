# Generated by Django 4.2.6 on 2024-03-11 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vookeys', '0009_requestbook_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issuebook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Issuedate', models.DateField(blank=True, null=True)),
                ('returndate', models.DateField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('issued', models.BooleanField(default=False)),
                ('returned', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vookeys.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
