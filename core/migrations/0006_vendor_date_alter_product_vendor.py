# Generated by Django 4.2.2 on 2024-01-20 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_alter_product_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="vendor",
            name="date",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="vendor",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="vendor",
                to="core.vendor",
            ),
        ),
    ]
