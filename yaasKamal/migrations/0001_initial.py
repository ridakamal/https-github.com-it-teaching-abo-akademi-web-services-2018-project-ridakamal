# Generated by Django 2.1.2 on 2018-10-28 16:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('creationDate', models.DateTimeField(default=datetime.datetime.now)),
                ('aLock', models.TextField(default='')),
                ('auctionOwner', models.CharField(max_length=25)),
                ('minPrice', models.FloatField()),
                ('deadline', models.DateTimeField(default=datetime.datetime(2018, 10, 31, 18, 37, 30, 634391))),
                ('adminBanned', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auctionOwner', models.CharField(max_length=100)),
                ('auctionKey', models.IntegerField()),
                ('bidOwner', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('createDate', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]
