# Generated by Django 4.2 on 2023-09-19 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gourmet_guide", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="shop",
            name="image",
            field=models.ImageField(null=True, upload_to="image/"),
        ),
    ]
