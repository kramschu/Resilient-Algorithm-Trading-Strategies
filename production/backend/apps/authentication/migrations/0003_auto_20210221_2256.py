# Generated by Django 3.1.6 on 2021-02-21 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20210221_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(editable=False, max_length=1000, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.AutoField(editable=False, max_length=1000, primary_key=True, serialize=False),
        ),
    ]
