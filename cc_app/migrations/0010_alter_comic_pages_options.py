# Generated by Django 4.1.3 on 2023-01-30 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cc_app", "0009_web_pages_header_img_url"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="Pages",
            options={
                "verbose_name": "Page",
                "verbose_name_plural": "Pages",
            },
        ),
    ]
