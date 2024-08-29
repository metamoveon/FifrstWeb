# Generated by Django 5.0.7 on 2024-08-23 14:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_order_not_complete_order_tracking_number_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=100, null=True)),
                ('product_id', models.CharField(blank=True, max_length=100, null=True)),
                ('product_name', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('total', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='cart_quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(blank=True, max_length=100, null=True)),
                ('product_name', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('stamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('total', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=100)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('tel', models.CharField(max_length=14)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.TextField()),
                ('express', models.CharField(max_length=100)),
                ('payment', models.CharField(max_length=100)),
                ('other', models.TextField(blank=True, null=True)),
                ('stamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('confirmed', models.BooleanField(default=False)),
                ('slip', models.ImageField(blank=True, null=True, upload_to='cart-slip/')),
                ('slip_time', models.DateTimeField(blank=True, null=True)),
                ('bank_account', models.CharField(choices=[('KBank', 'KBank'), ('SCB', 'SCB'), ('TTB', 'TTB'), ('KTB', 'KTB'), ('BAY', 'BAY'), ('อื่น', 'อื่น')], default='KBank', max_length=50)),
                ('payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('tracking_number', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
