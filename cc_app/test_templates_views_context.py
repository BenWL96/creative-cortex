import unittest, datetime, tempfile
from django.test import (
	Client,
	TestCase,
	SimpleTestCase
)
from django.urls import reverse, resolve
from . import views, models, utils, forms
from django.http import HttpResponseRedirect
from phonenumber_field.phonenumber import PhoneNumber

class testPatternNameResolveToView(unittest.TestCase):

	def test_Landing_Page_View(self):
		url = reverse('landing_page')
		self.assertEqual(resolve(url).func, views.Landing_Page)

	def test_Comics_View_No_Comics(self):
		url = reverse('comics')
		self.assertEqual(resolve(url).func, views.Comics)

	def test_Volumes_View_No_Comics(self):
		#If no comics exists go to landin pages
		kwargs = {"comic_param": "random-comic"}
		url = reverse('comic-detail', kwargs=kwargs)
		print(resolve(url).func)
		print(resolve(url).func)

	def test_Pages_View(self):
		url = reverse('pages')
		self.assertEqual(resolve(url).func, views.Pages)

	def test_Links_View(self):
		url = reverse('links')
		self.assertEqual(resolve(url).func, views.Links)

	def test_About_Us_View(self):
		url = reverse('about_us')
		self.assertEqual(resolve(url).func, views.About_Us)

	def test_Gallery_View(self):
		url = reverse('gallery')
		self.assertEqual(resolve(url).func, views.Gallery)

	"""Debug should be set to False before testing these
	
	def test_404_View(self):
		url = reverse('error_404')
		self.assertEqual(resolve(url).func, views.Error_404)

	def test_500_View(self):
		url = reverse('error_500')
		self.assertEqual(resolve(url).func, views.Error_500)
	
	"""

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

		self.assertTemplateUsed(response,'cc_app/comic_detail.html')
		self.assertTemplateUsed(response, 'cc_app/index.html')

	def test_Pages_Template(self):
		#Currently returns 400 status code, and I can't
		#Understand why.

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

class testContext(unittest.TestCase):

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
	unittest.main