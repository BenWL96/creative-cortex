# Generated by Django 4.1.6 on 2023-02-20 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cc_app", "0013_delete_images_volumes_volume_description"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comics",
            old_name="comic_img_376_by_376",
            new_name="comic_img_300_by_300",
        ),
    ]
