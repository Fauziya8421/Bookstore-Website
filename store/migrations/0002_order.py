# Generated by Django 4.0.6 on 2022-10-09 18:34

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.IntegerField()),
                ('email', models.CharField(max_length=40)),
                ('address', models.CharField(default='', max_length=50)),
                ('postal_code', models.CharField(default='', max_length=50)),
                ('state', models.CharField(default='', max_length=50)),
                ('contry', models.CharField(default='', max_length=50)),
                ('phone', models.CharField(default='', max_length=50)),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('status', models.BooleanField(default=False)),
                ('amount', models.ImageField(default=0, upload_to='')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.book')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.customer')),
            ],
        ),
    ]
