# Generated by Django 2.1.7 on 2019-03-07 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wasco_app', '0003_auto_20190307_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicedata',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='devicelocation',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
