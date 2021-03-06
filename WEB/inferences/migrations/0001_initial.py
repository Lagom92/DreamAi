# Generated by Django 3.1.1 on 2020-12-01 02:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('unit', models.CharField(max_length=50)),
                ('room', models.CharField(max_length=50)),
                ('birth', models.DateField()),
                ('admission', models.DateField()),
                ('sex', models.CharField(choices=[('male', '남성'), ('female', '여성')], max_length=50)),
                ('prescription', models.TextField(blank=True)),
                ('vitalSigns', models.TextField(blank=True)),
                ('history', models.TextField(blank=True)),
                ('etc', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Xray',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='img/%Y%m%d')),
                ('prediction', models.CharField(blank=True, max_length=100, null=True)),
                ('neg_rate', models.FloatField(blank=True, null=True)),
                ('pos_rate', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='xray', to='inferences.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Heat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='heat')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('xray', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='heat', to='inferences.xray')),
            ],
        ),
    ]
