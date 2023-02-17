# Generated by Django 4.1.3 on 2023-01-24 10:45

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import creative_cortex.storage_backends


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Chapters",
            fields=[
                ("chapter_id", models.AutoField(primary_key=True, serialize=False)),
                ("chapter_title", models.CharField(max_length=150)),
                ("slug_chapter_title", models.SlugField(max_length=170)),
                (
                    "chapter_number",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, message="value has to be above 0"
                            )
                        ]
                    ),
                ),
                (
                    "all_pages_exist_enable_displaying",
                    models.BooleanField(default=False),
                ),
            ],
            options={"verbose_name": "Chapter", "verbose_name_plural": "Chapters",},
        ),
        migrations.CreateModel(
            name="Comics",
            fields=[
                ("comic_id", models.AutoField(primary_key=True, serialize=False)),
                ("comic_name", models.CharField(max_length=150)),
                ("slug", models.SlugField(max_length=170)),
                ("comic_description", models.CharField(max_length=500)),
                ("comic_genre", models.CharField(max_length=150)),
                ("ongoing", models.BooleanField()),
                ("next_release_date", models.DateField()),
                (
                    "comic_img_376_by_376",
                    models.ImageField(
                        storage=creative_cortex.storage_backends.PrivateMediaStorage(),
                        upload_to="",
                    ),
                ),
                (
                    "comic_img_200_by_260",
                    models.ImageField(
                        storage=creative_cortex.storage_backends.PrivateMediaStorage(),
                        upload_to="",
                    ),
                ),
            ],
            options={"verbose_name": "Comic", "verbose_name_plural": "Comics",},
        ),
        migrations.CreateModel(
            name="Gallery_images",
            fields=[
                ("gallery_img_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "gallery_img_placement_number",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, message="value has to be above 0"
                            )
                        ]
                    ),
                ),
                ("gallery_img_description", models.CharField(max_length=200)),
                (
                    "gallery_img_486_by_165",
                    models.ImageField(
                        storage=creative_cortex.storage_backends.PrivateMediaStorage(),
                        upload_to="",
                    ),
                ),
            ],
            options={
                "verbose_name": "Gallery Image",
                "verbose_name_plural": "Gallery Images",
            },
        ),
        migrations.CreateModel(
            name="Landing_Page_Images",
            fields=[
                (
                    "landing_page_img_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                (
                    "landing_page_img_carousel_placement_number",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, message="value has to be above 0"
                            )
                        ]
                    ),
                ),
                ("landing_page_img_description", models.CharField(max_length=50)),
                (
                    "landing_page_img_n_by_n",
                    models.ImageField(
                        storage=creative_cortex.storage_backends.PrivateMediaStorage(),
                        upload_to="",
                    ),
                ),
            ],
            options={
                "verbose_name": "Landing Page Image",
                "verbose_name_plural": "Landing Page Images",
            },
        ),
        migrations.CreateModel(
            name="Personnel",
            fields=[
                ("personnel_id", models.AutoField(primary_key=True, serialize=False)),
                ("full_name", models.CharField(max_length=75, unique=True)),
                ("phone_number", models.IntegerField()),
                ("email_address", models.EmailField(max_length=254)),
                ("role_at_creative_cortex", models.CharField(max_length=20)),
                (
                    "person_img_200_by_260",
                    models.ImageField(
                        storage=creative_cortex.storage_backends.PrivateMediaStorage(),
                        upload_to="",
                    ),
                ),
            ],
            options={"verbose_name": "Personnel", "verbose_name_plural": "Personnel",},
        ),
        migrations.CreateModel(
            name="Volumes",
            fields=[
                ("volume_id", models.AutoField(primary_key=True, serialize=False)),
                ("volume_title", models.CharField(max_length=150)),
                ("slug_volume_title", models.SlugField(max_length=170)),
                (
                    "vol_number",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, message="value has to be above 0"
                            )
                        ]
                    ),
                ),
                ("date_published", models.DateField()),
                (
                    "comic_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cc_app.comics"
                    ),
                ),
            ],
            options={"verbose_name": "Volume", "verbose_name_plural": "Volumes",},
        ),
        migrations.CreateModel(
            name="Pages",
            fields=[
                ("page_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "page_number",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, message="value has to be above 0"
                            )
                        ]
                    ),
                ),
                (
                    "page_img",
                    models.ImageField(
                        storage=creative_cortex.storage_backends.PrivateMediaStorage(),
                        upload_to="",
                    ),
                ),
                (
                    "chapter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cc_app.chapters",
                    ),
                ),
            ],
            options={"verbose_name": "Page", "verbose_name_plural": "Pages",},
        ),
        migrations.CreateModel(
            name="Comic_Personnel",
            fields=[
                (
                    "comic_personnel_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("Artist", "Artist"),
                            ("Author", "Author"),
                            ("Artist & Author", "Artist & Author"),
                        ],
                        max_length=40,
                    ),
                ),
                (
                    "comic_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cc_app.comics"
                    ),
                ),
                (
                    "personnel_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cc_app.personnel",
                    ),
                ),
            ],
            options={
                "verbose_name": "Comic Personnel",
                "verbose_name_plural": "Comic Personnel",
            },
        ),
        migrations.AddField(
            model_name="chapters",
            name="volume",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="cc_app.volumes"
            ),
        ),
    ]
