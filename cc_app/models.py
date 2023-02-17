from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField

from creative_cortex.storage_backends import PrivateMediaStorage


class Comics(models.Model):

    comic_id = models.AutoField(primary_key=True)
    comic_name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170)
    comic_description = models.CharField(max_length=500)
    comic_genre = models.CharField(max_length=150)
    ongoing = models.BooleanField()
    next_release_date = models.DateField()
    # initial_release_date = models.DateField()
    comic_img_376_by_376 = models.ImageField(storage=PrivateMediaStorage())
    comic_img_200_by_260 = models.ImageField(storage=PrivateMediaStorage())
    display_comic = models.BooleanField(default=False)

    def __str__(self):
        return self.comic_name

    class Meta:
        verbose_name = "Comic"
        verbose_name_plural = "Comics"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.comic_name)
        return super().save(*args, **kwargs)


class Volumes(models.Model):

    volume_id = models.AutoField(primary_key=True)
    comic_name = models.ForeignKey(Comics, on_delete=models.CASCADE)
    volume_title = models.CharField(max_length=150)
    # volume_description = models.CharField(max_length=500)
    slug_volume_title = models.SlugField(max_length=170)
    vol_number = models.IntegerField(validators=[
        MinValueValidator(1, message="value has to be above 0"),
    ])
    date_published = models.DateField()
    # volume_img = models.FileField()

    def __str__(self):
        return self.comic_name.comic_name + " | volume " + str(self.vol_number)

    class Meta:
        verbose_name = "Volume"
        verbose_name_plural = "Volumes"

    def save(self, *args, **kwargs):
        if not self.slug_volume_title:
            self.slug = slugify(self.volume_title)
        return super().save(*args, **kwargs)


class Chapters(models.Model):

    chapter_id = models.AutoField(primary_key=True)
    volume = models.ForeignKey(Volumes, on_delete=models.CASCADE)
    chapter_title = models.CharField(max_length=150)
    slug_chapter_title = models.SlugField(max_length=170)
    chapter_number = models.IntegerField(validators=[
        MinValueValidator(1, message="value has to be above 0"),
    ])
    all_pages_exist_enable_displaying = models.BooleanField(default=False)

    def __str__(self):
        return self.volume.comic_name.comic_name + \
            " | volume " + str(self.volume.vol_number) + \
            " | chapter " + str(self.chapter_number)

    class Meta:
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"

    def save(self, *args, **kwargs):
        if not self.slug_chapter_title:
            self.slug = slugify(self.chapter_title)
        return super().save(*args, **kwargs)


class Pages(models.Model):

    page_id = models.AutoField(primary_key=True)
    # Volume is associated with comic, so we need to perform a prefetch
    chapter = models.ForeignKey(Chapters, on_delete=models.CASCADE)
    page_number = models.IntegerField(validators=[
        MinValueValidator(1, message="value has to be above 0"),
    ])
    page_img = models.ImageField(storage=PrivateMediaStorage())

    def __str__(self):
        return self.chapter.volume.comic_name.comic_name + \
            " | volume " + str(self.chapter.volume.vol_number) + \
            " | chapter " + str(self.chapter.chapter_number) + \
            " | page " + str(self.page_number)

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"


class Personnel(models.Model):

    personnel_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=75, unique=True)
    phone_number = PhoneNumberField(blank=True, unique=True)
    email_address = models.EmailField()
    role_at_creative_cortex = models.CharField(max_length=20)
    person_img_200_by_260 = models.ImageField(storage=PrivateMediaStorage())

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Personnel"
        verbose_name_plural = "Personnel"


CHOICES = (
    ('Artist', "Artist"),
    ("Author", "Author"),
    ("Artist & Author", "Artist & Author")
)

class Comic_Personnel(models.Model):

    comic_personnel_id = models.AutoField(primary_key=True)
    personnel_id = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    comic_id = models.ForeignKey(Comics, on_delete=models.CASCADE)
    role = models.CharField(choices=CHOICES, max_length=40)
    # photograph = models.FileField()

    def __str__(self):
        return self.personnel_id.full_name

    class Meta:
        verbose_name = "Comic Personnel"
        verbose_name_plural = "Comic Personnel"


class Landing_Page_Images(models.Model):

    landing_page_img_id = models.AutoField(primary_key=True)
    landing_page_img_carousel_placement_number = models.IntegerField(
        validators=[MinValueValidator(1, message="value has to be above 0"),]
    )
    landing_page_img_description = models.CharField(max_length=50)
    landing_page_img_n_by_n = models.ImageField(storage=PrivateMediaStorage())

    def __str__(self):
        return "img: " + \
            str(self.landing_page_img_carousel_placement_number) + \
            " | " + self.landing_page_img_description

    class Meta:
        verbose_name = "Landing Page Image"
        verbose_name_plural = "Landing Page Images"


class Gallery_images(models.Model):

    gallery_img_id = models.AutoField(primary_key=True)
    gallery_img_placement_number = models.IntegerField(validators=[
        MinValueValidator(1, message="value has to be above 0"),
    ])
    gallery_img_description = models.CharField(max_length=200)
    gallery_img_url = models.ImageField(storage=PrivateMediaStorage())

    def __str__(self):
        return "img: " + str(self.gallery_img_placement_number) + \
            " | " + self.gallery_img_description

    class Meta:
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"


# Related to adding content to webpages.
class Web_Pages(models.Model):

    id = models.AutoField(primary_key=True)
    page_name = models.CharField(max_length=25, unique=True)
    header_img_url = models.ImageField(
        storage=PrivateMediaStorage(),
        null=True
    )

    def __str__(self):
        return self.page_name

    class Meta:
        verbose_name = "Web Page"
        verbose_name_plural = "Web Pages"


class Web_Page_Text_Content(models.Model):

    id = models.AutoField(primary_key=True)
    page_name = models.ForeignKey(Web_Pages, on_delete=models.CASCADE)
    text_content_ordering = models.IntegerField(validators=[
        MinValueValidator(1, message="value has to be above 0"),
    ])
    text_content = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.page_name.page_name + \
            " | " + str(self.text_content_ordering)

    class Meta:
        verbose_name = "Text Content For WebPages"
        verbose_name_plural = "Text Content For WebPages"


class Featured_Youtube_videos(models.Model):

    id = models.AutoField(primary_key=True)
    video_name = models.CharField(max_length=50)
    video_ordering = models.IntegerField(
        validators=[MinValueValidator(1, message="value has to be above 0"), ])
    url = models.URLField()

    def __str__(self):
        return str(self.video_ordering) + " | " + self.video_name

    class Meta:
        verbose_name = "Featured Youtube video"
        verbose_name_plural = "Featured Youtube videos"


class Inquiries(models.Model):

    inquiry_id = models.AutoField(primary_key=True)
    inquiry = models.CharField(max_length=150)
    name = models.CharField(max_length=50, default="")
    email = models.EmailField()
    checked = models.BooleanField(default=False)

    def __str__(self):
        return "Inquiry: " + str(self.inquiry_id) + \
            " | from " + self.email + \
            " | checked: " + str(self.checked)

    class Meta:
        verbose_name = "Inquiry"
        verbose_name_plural = "Inquiries"
