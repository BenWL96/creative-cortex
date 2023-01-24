# Generated by Django 4.1.3 on 2023-01-24 14:46

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("cc_app", "0002_rename_gallery_img_486_by_165_gallery_images_gallery_img_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="personnel",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=128, region=None, unique=True
            ),
        ),
    ]