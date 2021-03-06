# Generated by Django 2.1.5 on 2019-01-13 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0004_client_previous_credit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.IntegerField(default=0)),
                ('inventory', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='bills.Inventory')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_item', to='bills.Product')),
            ],
        ),
    ]
