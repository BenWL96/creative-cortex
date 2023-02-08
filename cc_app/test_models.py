import datetime, tempfile
from django.test import (
	TestCase,
)
from . import models
from phonenumber_field.phonenumber import PhoneNumber


class testModelFieldParameters(TestCase):

	def test_volume_number_model_cant_be_negative(self):

		a_simple_file = tempfile.NamedTemporaryFile(suffix=".jpg").name

		comic_object = models.Comics.objects.create(
			comic_name="comic_1",
			comic_description="description",
			comic_genre="genre",
			ongoing=True,
			next_release_date=datetime.date.today(),
			comic_img_376_by_376=a_simple_file,
			comic_img_200_by_260=a_simple_file,
			display_comic=True
		)
		volume_object = models.Volumes.objects.create(
			comic_name=comic_object,
			volume_title="title",
			vol_number=-1,
			date_published=datetime.date.today()
		)

		"""Here we need to test the volume object does not exist"""
		"""And instead that an error is raised"""


if __name__ == "__main__":
	unittest.main()