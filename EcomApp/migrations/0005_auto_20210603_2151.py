# Generated by Django 3.1.7 on 2021-06-03 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcomApp', '0004_auto_20210310_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='phone',
            field=models.TextField(),
        ),
    ]
