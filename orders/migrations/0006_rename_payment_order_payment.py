# Generated by Django 4.1 on 2022-08-27 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_remove_orderproduct_variation_orderproduct_variation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Payment',
            new_name='payment',
        ),
    ]