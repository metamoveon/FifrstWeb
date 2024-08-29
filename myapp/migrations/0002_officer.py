# Generated by Django 5.0.7 on 2024-07-31 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Officer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('tel', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('other', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
