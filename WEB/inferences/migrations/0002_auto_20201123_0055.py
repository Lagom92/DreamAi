# Generated by Django 3.1 on 2020-11-22 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inferences', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='history',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='prescription',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='vitalSigns',
            field=models.TextField(blank=True),
        ),
    ]
