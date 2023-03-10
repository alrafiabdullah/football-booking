# Generated by Django 3.2.16 on 2022-12-16 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=999)),
                ('map_link', models.URLField(max_length=9999)),
            ],
            options={
                'verbose_name_plural': 'Places',
            },
        ),
    ]
