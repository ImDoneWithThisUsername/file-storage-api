# Generated by Django 4.1.6 on 2023-02-21 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='n',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='public_key',
            field=models.IntegerField(null=True),
        ),
    ]
