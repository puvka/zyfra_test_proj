# Generated by Django 4.0.4 on 2022-04-18 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='extras',
            field=models.JSONField(null=True, verbose_name='Доп.данные о грузе'),
        ),
    ]
