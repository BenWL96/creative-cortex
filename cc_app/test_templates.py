import datetime
import tempfile

from django.test import Client, TestCase
from django.urls import reverse
from phonenumber_field.phonenumber import PhoneNumber

from . import models


class testViewsAndTemplates(TestCase):

	def setUp(self):
		self.client = Client()
		self.a_simple_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
		phone_number = "+447713835916"
		self.number = PhoneNumber.from_string(phone_number, region=None)

	def test_Homepage_Template(self):
		response = self.client.get(reverse('landing_page'))
		self.assertEqual(response.status_code, 200)

		self.assertTemplateUsed(response, "cc_app/landing_page.html")
		self.assertTemplateUsed(response, "cc_app/index.html")

	def test_Comics_Template(self):
		response = self.client.get(reverse('comics'))
		self.assertEqual(response.status_code, 200)

		self.assertTemplateUsed(response, 'cc_app/comics.html')
		self.assertTemplateUsed(response, 'cc_app/index.html')

	def test_Volumes_template(self):
		comic_object = models.Comics.objects.create(
			comic_name="comic_1",
			ongoing=True,
			next_release_date=datetime.date.today(),
			display_comic=True
		)
		kwargs = {"comic_param": comic_object.slug}

		response = self.client.get(reverse('comic-detail', kwargs=kwargs))
		self.assertEqual(response.status_code, 200)

		self.assertTemplateUsed(response, 'cc_app/comic_detail.html')
		self.assertTemplateUsed(response, 'cc_app/index.html')

	def test_Pages_Template(self):
		# Currently returns 400 status code, and I can't
		# Understand why.

		comic_object = models.Comics.objects.create(
			comic_name="comic",
			comic_description="something",
			comic_genre="something",
			ongoing=True,
			next_release_date=datetime.date.today(),
			comic_img_376_by_376=self.a_simple_file,
			comic_img_200_by_260=self.a_simple_file,
			display_comic=True
		)
		volume_object = models.Volumes.objects.create(
			comic_name=comic_object,
			volume_title="volume title",
			vol_number=1,
			date_published=datetime.date.today()
		)
		chapters_object = models.Chapters.objects.create(
			volume=volume_object,
			chapter_title="chapter title",
			chapter_number=1,
			all_pages_exist_enable_displaying=True
		)

		pages_object = models.Pages.objects.create(
			chapter=chapters_object,
			page_number=1,
			page_img=self.a_simple_file
		)
		kwargs = {
			"comic_param": comic_object.slug,
			"volume_param": volume_object.vol_number,
			"chapter_param": chapters_object.chapter_number,
			"page_param": pages_object.page_number
		}

		response = self.client.get(reverse('pages', kwargs=kwargs))
		self.assertEqual(response.status_code, 200)

		print(response)

		self.assertTemplateUsed(response, 'cc_app/pages.html')
		self.assertTemplateUsed(response, 'cc_app/index.html')

	def test_Links_Template(self):
		page_name = models.Web_Pages.objects.create(page_name="Links")
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

		response = self.client.get(reverse('links'))
		self.assertEqual(response.status_code, 200)

		self.assertTemplateUsed(response, 'cc_app/links.html')
		self.assertTemplateUsed(response, 'cc_app/index.html')

	def test_About_Us_Template(self):
		page_name = models.Web_Pages.objects.create(
			page_name="About Us",
			header_img_url=self.a_simple_file
		)
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
		print(response)
		print(response)
		self.assertEqual(response.status_code, 200)

		self.assertTemplateUsed(response, 'cc_app/about_us.html')
		self.assertTemplateUsed(response, 'cc_app/index.html')

	def test_Gallery_Template(self):
		response = self.client.get(reverse('gallery'))
		self.assertEqual(response.status_code, 200)

		self.assertTemplateUsed(response, 'cc_app/gallery.html')
		self.assertTemplateUsed(response, 'cc_app/index.html')

	"""Debug should be set to False before testing these

	def test_404_template(self):
		#This Test Is Failing
		response = self.client.get(reverse('error_404'))
		self.assertEqual(response.status_code, 200)

		self.assertTemplateUsed(response,
								template_name='cc_app/error_404.html')



	def test_500_Template(self):

		response = self.client.get(reverse('error_500'))
		self.assertEqual(response.status_code, 200)

		self.assertTemplateUsed(response,
								template_name='cc_app/error_500.html')
	"""


if __name__ == "__main__":
	unittest.main()
