# Generated by Django 4.2.2 on 2024-01-19 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_rename_price_product_vendor_price_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="vendor",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.vendor",
            ),
        ),
    ]
