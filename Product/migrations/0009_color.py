# Generated by Django 3.1.7 on 2021-06-17 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0008_auto_20210603_2151'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]