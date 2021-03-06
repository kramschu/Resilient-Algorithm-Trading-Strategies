# Generated by Django 3.1.6 on 2021-02-20 01:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Backtest',
            fields=[
                ('backtestid', models.AutoField(primary_key=True, serialize=False)),
                ('algname', models.CharField(max_length=30)),
                ('cash', models.DecimalField(decimal_places=2, max_digits=11)),
                ('buytol', models.DecimalField(decimal_places=5, max_digits=10)),
                ('selltol', models.DecimalField(decimal_places=5, max_digits=10)),
                ('startdate', models.CharField(max_length=10)),
                ('enddate', models.CharField(max_length=10)),
                ('filepath', models.CharField(max_length=50)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quant_connect.user')),
            ],
        ),
    ]
