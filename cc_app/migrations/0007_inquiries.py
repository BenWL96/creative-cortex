# Generated by Django 4.1.3 on 2023-01-26 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cc_app", "0006_featured_youtube_videos_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Inquiries",
            fields=[
                ("inquiry_id", models.AutoField(primary_key=True, serialize=False)),
                ("inquiry", models.CharField(max_length=150)),
                ("email", models.EmailField(max_length=254)),
                ("checked", models.BooleanField(default=False)),
            ],
            options={"verbose_name": "Inquiry", "verbose_name_plural": "Inquiries",},
        ),
    ]
