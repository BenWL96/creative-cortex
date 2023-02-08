import datetime, tempfile
from django.test import (
	Client,
	TestCase
)
from django.urls import reverse, resolve
from . import views, models, utils, forms
from phonenumber_field.phonenumber import PhoneNumber

class testContext(TestCase):

	def setUp(self):

		self.a_simple_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
		self.client = Client()
		phone_number = "+447713835916"
		self.number = PhoneNumber.from_string(phone_number, region=None)

	def test_landing_page_context(self):

		models.Landing_Page_Images.objects.create(
			landing_page_img_carousel_placement_number=1,
			landing_page_img_description="image number 1",
			landing_page_img_n_by_n=self.a_simple_file
		)

		response = self.client.get(reverse('landing_page'))
		context_objects = response.context['carousel_img_objects']
		print(context_objects)
		self.assertEqual(len(context_objects), 1)

	def test_comic_page_context(self):

		models.Comics.objects.create(
			comic_name="comic_1",
			ongoing=True,
			next_release_date=datetime.date.today(),
			comic_img_376_by_376=self.a_simple_file,
			comic_img_200_by_260=self.a_simple_file,
			display_comic=True
		)

		response = self.client.get(reverse('comics'))
		context_objects = response.context['comics']
		self.assertEqual(len(context_objects), 1)

	def test_about_us_page_context(self):

		page_name = models.Web_Pages.objects.create(page_name="About Us")
		models.Web_Page_Text_Content.objects.create(
			page_name=page_name,
			text_content_ordering=1,
			text_content="ipsum"
		)
		models.Personnel.objects.create(
			full_name="x",
			phone_number=self.number,
			email_address="y@gmail.com",
			role_at_creative_cortex="Founder",
			person_img_200_by_260=self.a_simple_file
		)

		response = self.client.get(reverse('about_us'))
		context_object_person = response.context['personnel']
		context_object_text = response.context['page_text_content_1']

		self.assertEqual(len(context_object_person), 1)
		self.assertIsNotNone(context_object_text)


	def test_about_us_page_context_2_text(self):

		page_name = models.Web_Pages.objects.get(page_name="About Us")

		models.Web_Page_Text_Content.objects.create(
			page_name=page_name,
			text_content_ordering=2,
			text_content="ipsum"
		)

		response = self.client.get(reverse('about_us'))
		context_object_person = response.context['personnel']
		context_object_text = response.context['page_text_content_1']
		context_object_text_2 = response.context['page_text_content_2']
		self.assertEqual(len(context_object_person), 1)
		self.assertIsNotNone(context_object_text)
		self.assertIsNotNone(context_object_text_2)




	"""def test_about_page_context(self):

		raw_phone = "+447713835911"
		phone_num = PhoneNumber.from_string(phone_number=raw_phone).as_e164

		models.Personnel.objects.create(

			full_name="name",
			phone_number=phone_num,
			email_address="name@email.com",
			role_at_creative_cortex="founder",
			person_img_200_by_260=self.a_simple_file
		)

		about_page_object = models.Web_Pages.objects.create(
			page_name="About Page"
		)

		models.Web_Pages.objects.create(
			page_name=about_page_object,
			text_content_ordering=1,
			text_content="lorem ipsum"

		)

		response = self.client.get(reverse('about_us'))
		context_objects = response.context['personnel']
		self.assertEqual(len(context_objects), 1)
		context_objects = response.context['page_text_content_1']
		self.assertEqual(len(context_objects), 1)"""



if __name__ == "__main__":
	unittest.main()