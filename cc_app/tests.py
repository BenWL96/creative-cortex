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
	"""
	def test_Pages_View(self):
		url = reverse('pages')
		self.assertEqual(resolve(url).func, views.Pages)"""

	def test_Links_View(self):
		url = reverse('links')
		self.assertEqual(resolve(url).func, views.Links)

	def test_About_Us_View(self):
		url = reverse('about_us')
		self.assertEqual(resolve(url).func, views.About_Us)

	def test_Gallery_View(self):
		url = reverse('gallery')
		self.assertEqual(resolve(url).func, views.Gallery)

	"""def test_404_View(self):
		url = reverse('error_404')
		self.assertEqual(resolve(url).func, views.Error_404)

	def test_500_View(self):
		url = reverse('error_500')
		self.assertEqual(resolve(url).func, views.Error_500)"""

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
			next_release_date=datetime.date.today()
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
			comic_img_200_by_260=self.a_simple_file
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
		self.assertEqual(response.status_code, 200)

		self.assertTemplateUsed(response, 'cc_app/about_us.html')
		self.assertTemplateUsed(response, 'cc_app/index.html')

	def test_Gallery_Template(self):

		response = self.client.get(reverse('gallery'))
		self.assertEqual(response.status_code, 200)

		self.assertTemplateUsed(response, 'cc_app/gallery.html')


	"""def test_404_template(self):
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


class testUtils(TestCase):

	def setUp(self):

		phone_number = "+447788888884"
		phone_number_2 = "+447788888885"
		phone_number_3 = "+447788888889"
		self.number = PhoneNumber.from_string(phone_number, region=None)
		self.number_2 = PhoneNumber.from_string(phone_number_2, region=None)
		self.number_3 = PhoneNumber.from_string(phone_number_3, region=None)

		self.a_simple_file = tempfile.NamedTemporaryFile(suffix=".jpg").name

	def test_return_chapters_related_to_volumes_queryset(self):

		comic_object = models.Comics.objects.create(
			comic_name="comic_1",
			ongoing=True,
			next_release_date=datetime.date.today()
		)

		volume_object = models.Volumes.objects.create(
			comic_name=comic_object,
			volume_title="Volume Name",
			vol_number=1,
			date_published=datetime.date.today()
		)

		models.Chapters.objects.create(
			volume=volume_object,
			chapter_title="Chapter Name 1",
			chapter_number=1,
		)

		models.Chapters.objects.create(
			volume=volume_object,
			chapter_title="Chapter Name 2",
			chapter_number=2,
		)

		volumes_related = models.Volumes.objects.select_related(
			'comic_name').filter(comic_name=comic_object)

		chapters_related = utils.return_chapters_related_to_volumes_queryset(volumes_related)
		chapters_related_count = len(chapters_related)
		self.assertEqual(chapters_related_count, 2)

	def test_type_param_comic_slug_boolean_false(self):
		comic_param = 1512
		type_check_passed = utils.check_type_param_comic_slug_boolean(comic_param)
		self.assertEqual(type_check_passed, False)

	def test_type_param_comic_slug_boolean_true(self):
		comic_param = 'comic-123'
		type_check_passed = utils.check_type_param_comic_slug_boolean(comic_param)
		self.assertEqual(type_check_passed, True)

	def test_check_type_volume_param_boolean_false(self):
		volume_param = "abc"
		type_check_passed = utils.check_type_volume_param_boolean(volume_param)
		self.assertEqual(type_check_passed, False)

	def test_check_type_volume_param_boolean_true(self):
		volume_param = 1512
		type_check_passed = utils.check_type_volume_param_boolean(volume_param)
		self.assertEqual(type_check_passed, True)

	def test_check_type_chapter_param_boolean_false(self):
		chapter_param = "abc"
		type_check_passed = utils.check_type_chapter_param_boolean(chapter_param)
		self.assertEqual(type_check_passed, False)

	def test_check_type_chapter_param_boolean_true(self):
		chapter_param = 1512
		type_check_passed = utils.check_type_chapter_param_boolean(chapter_param)
		self.assertEqual(type_check_passed, True)

	def test_check_type_page_param_boolean_false(self):
		page_param = "abc"
		type_check_passed = utils.check_type_page_param_boolean(page_param)
		self.assertEqual(type_check_passed, False)

	def test_check_type_page_param_boolean_true(self):
		page_param = 1512
		type_check_passed = utils.check_type_page_param_boolean(page_param)
		self.assertEqual(type_check_passed, True)



	def test_find_chapter_from_params_or_redirect_NO_OBJECTS(self):
		comic_param, volume_param, chapter_param, page_param = "comic_1", 1, 1, 1
		response = utils.find_chapter_with_all_pages_from_params_or_redirect(
			comic_param,
			volume_param,
			chapter_param,
			page_param
		)
		self.assertEqual(response.status_code, 302)

	def test_find_chapter_with_all_pages_from_params_or_redirect_COMIC_NO_OTHER_OBJECTS(self):

		comic = models.Comics.objects.create(
			comic_name="comic_1",
			ongoing=True,
			next_release_date=datetime.date.today(),
			comic_img_376_by_376=self.a_simple_file,
			comic_img_200_by_260=self.a_simple_file
		)
		comic_name = comic.comic_name
		comic_param, volume_param, chapter_param, page_param = comic_name, 1, 1, "false"
		response = utils.find_chapter_with_all_pages_from_params_or_redirect(
			comic_param,
			volume_param,
			chapter_param,
			page_param
		)
		self.assertEqual(response.status_code, 302)

	def test_find_chapter_from_params_or_redirect_COMIC_VOLUME_NO_OTHER_OBJECTS(self):

		comic_object = models.Comics.objects.create(
			comic_name="comic_1",
			ongoing=True,
			next_release_date=datetime.date.today(),
			comic_img_376_by_376=self.a_simple_file,
			comic_img_200_by_260=self.a_simple_file
		)

		models.Volumes.objects.create(
			comic_name=comic_object,
			volume_title="Volume Name",
			vol_number=1,
			date_published=datetime.date.today()
		)

		comic_param, volume_param, chapter_param, page_param = "comic_1", 1, 1, "false"
		response = utils.find_chapter_with_all_pages_from_params_or_redirect(
			comic_param,
			volume_param,
			chapter_param,
			page_param
		)
		self.assertEqual(response.status_code, 302)

	def test_find_chapter_from_params_or_redirect_COMIC_VOLUME_CHAPTER_OBJECTS(self):

		comic_object = models.Comics.objects.create(
			comic_name="comic_1",
			ongoing=True,
			next_release_date=datetime.date.today(),
			comic_img_376_by_376=self.a_simple_file,
			comic_img_200_by_260=self.a_simple_file
		)

		volume_object = models.Volumes.objects.create(
			comic_name=comic_object,
			volume_title="Volume Name",
			vol_number=1,
			date_published=datetime.date.today()
		)

		chapter_object = models.Chapters.objects.create(
			volume=volume_object,
			chapter_title="Chapter Name 1",
			chapter_number=1,
		)

		comic_name = comic_object.comic_name
		volume_number = volume_object.vol_number
		chapter_number = chapter_object.chapter_number


		comic_param, volume_param, chapter_param, page_param = comic_name, volume_number, chapter_number, 1
		response = utils.find_chapter_with_all_pages_from_params_or_redirect(
			comic_param,
			volume_param,
			chapter_param,
			page_param
		)
		self.assertEqual(type(response), HttpResponseRedirect)

	def test_take_volumes_of_comic_return_list_volumes_with_chapters(self):

		comic_object = models.Comics.objects.create(
			comic_name="comic_1",
			ongoing=True,
			next_release_date=datetime.date.today(),
			comic_img_376_by_376=self.a_simple_file,
			comic_img_200_by_260=self.a_simple_file
		)

		volume_object = models.Volumes.objects.create(
			comic_name=comic_object,
			volume_title="Volume Name",
			vol_number=1,
			date_published=datetime.date.today()
		)

		chapter_object = models.Chapters.objects.create(
			volume=volume_object,
			chapter_title="Chapter Name 1",
			chapter_number=1,
		)
		models.Pages.objects.create(
			chapter=chapter_object,
			page_number=1,
			page_img=self.a_simple_file
		)

		volumes_related_to_comic_param = [volume_object]

		list_volumes_with_chapters_and_pages = utils.take_volumes_with_chap_return_list_volumes_that_have_chapters_and_pages(volumes_related_to_comic_param)
		print(list_volumes_with_chapters_and_pages)
		self.assertEqual(len(list_volumes_with_chapters_and_pages), 1)

	def test_take_NO_volumes_of_comic_return_list_volumes_with_chapters(self):

		volumes_related_to_comic_param = []

		list_volumes_with_chapters_and_pages = utils.take_volumes_with_chap_return_list_volumes_that_have_chapters_and_pages(volumes_related_to_comic_param)
		print(list_volumes_with_chapters_and_pages)
		self.assertEqual(len(list_volumes_with_chapters_and_pages), 0)


	def test_take_volumes_with_chap_return_list_volumes_that_have_chapters_and_pages(self):

		comic_object = models.Comics.objects.create(
			comic_name="comic_1",
			ongoing=True,
			next_release_date=datetime.date.today(),
			comic_img_376_by_376=self.a_simple_file,
			comic_img_200_by_260=self.a_simple_file
		)

		volume_object = models.Volumes.objects.create(
			comic_name=comic_object,
			volume_title="Volume Name",
			vol_number=1,
			date_published=datetime.date.today()
		)

		chapter_object = models.Chapters.objects.create(
			volume=volume_object,
			chapter_title="Chapter Name 1",
			chapter_number=1,
		)
		models.Pages.objects.create(
			chapter=chapter_object,
			page_number=1,
			page_img=self.a_simple_file
		)

		list_volumes_with_chapters = [volume_object]

		list_volumes_with_chapters_and_pages = utils.take_volumes_with_chap_return_list_volumes_that_have_chapters_and_pages(list_volumes_with_chapters)
		print(list_volumes_with_chapters_and_pages)
		self.assertEqual(len(list_volumes_with_chapters_and_pages), 1)

	def test_take_NO_volumes_with_chap_return_list_volumes_that_have_chapters_and_pages(self):

		list_volumes_with_chapters = []

		list_volumes_with_chapters_and_pages = utils.take_volumes_with_chap_return_list_volumes_that_have_chapters_and_pages(list_volumes_with_chapters)
		print(list_volumes_with_chapters_and_pages)
		self.assertEqual(len(list_volumes_with_chapters_and_pages), 0)

	def test_assign_personnel_objects_even_boolean_return_correct_length_list(self):

		models.Personnel.objects.create(
			full_name="name goes here",
			phone_number=self.number,
			email_address="name@gmail.com",
			role_at_creative_cortex='Founder',
			person_img_200_by_260=self.a_simple_file
		)
		models.Personnel.objects.create(
			full_name="name goes here 2",
			phone_number=self.number_2,
			email_address="name@gmail.com",
			role_at_creative_cortex='Founder',
			person_img_200_by_260=self.a_simple_file
		)

		personnel_list = utils.assign_personnel_objects_even_boolean_return_list()
		self.assertEqual(len(personnel_list), 2)

	def test_check_even_values_from_assign_personnel_objects_even_boolean_return(self):

		models.Personnel.objects.create(
			full_name="name goes here",
			phone_number=self.number,
			email_address="name@gmail.com",
			role_at_creative_cortex='Founder',
			person_img_200_by_260=self.a_simple_file
		)
		models.Personnel.objects.create(
			full_name="name goes here 2",
			phone_number=self.number_2,
			email_address="name@gmail.com",
			role_at_creative_cortex='Founder',
			person_img_200_by_260=self.a_simple_file
		)

		models.Personnel.objects.create(
			full_name="name goes here 3",
			phone_number=self.number_3,
			email_address="name@gmail.com",
			role_at_creative_cortex='Founder',
			person_img_200_by_260=self.a_simple_file
		)

		personnel_list = utils.assign_personnel_objects_even_boolean_return_list()

		first_person = personnel_list[0]
		second_person = personnel_list[1]
		third_person = personnel_list[2]

		first_person_not_even = first_person.even == 'false'
		second_person_even = second_person.even == "true"
		third_person_not_even = third_person.even == 'false'


		self.assertEqual(first_person_not_even, True)
		self.assertEqual(second_person_even, True)
		self.assertEqual(third_person_not_even, True)

	def test_Pass_Links_Text_Return_Context(self):

		featured_video = models.Featured_Youtube_videos.objects.create(
			video_name="vid 1",
			video_ordering=1,
			url="https://www.youtube.com/embed/Hf75Q0ir39w"
		)
		page_name = models.Web_Pages.objects.create(page_name="Links")
		models.Web_Page_Text_Content.objects.create(
			page_name=page_name,
			text_content_ordering=1,
			text_content="ipsum"
		)
		models.Web_Page_Text_Content.objects.create(
			page_name=page_name,
			text_content_ordering=2,
			text_content="ipsum"
		)

		web_page_text_objects = models.Web_Page_Text_Content.objects.all()
		context = utils.Pass_Links_Text_Return_Context(
			featured_video,
			web_page_text_objects
		)


		self.assertEqual(len(context), 3)

	def test_Pass_About_Us_Text_Return_Context(self):

		models.Personnel.objects.create(
			full_name="name goes here",
			phone_number=self.number,
			email_address="name@gmail.com",
			role_at_creative_cortex='Founder',
			person_img_200_by_260=self.a_simple_file
		)
		models.Personnel.objects.create(
			full_name="name goes here 2",
			phone_number=self.number_2,
			email_address="name@gmail.com",
			role_at_creative_cortex='Founder',
			person_img_200_by_260=self.a_simple_file
		)

		models.Personnel.objects.create(
			full_name="name goes here 3",
			phone_number=self.number_3,
			email_address="name@gmail.com",
			role_at_creative_cortex='Founder',
			person_img_200_by_260=self.a_simple_file
		)

		page_name = models.Web_Pages.objects.create(page_name="About Us")
		models.Web_Page_Text_Content.objects.create(
			page_name=page_name,
			text_content_ordering=1,
			text_content="ipsum"
		)
		models.Web_Page_Text_Content.objects.create(
			page_name=page_name,
			text_content_ordering=2,
			text_content="ipsum"
		)

		web_page_text_objects = models.Web_Page_Text_Content.objects.all()
		personnel = models.Personnel.objects.all()
		context = utils.Pass_About_Us_Text_Return_Context(personnel, web_page_text_objects)
		print(context)

class testContext(unittest.TestCase):

	def setUp(self):

		self.a_simple_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
		self.client = Client()
		phone_number = "+447713835916"
		self.number = PhoneNumber.from_string(phone_number, region=None)

		"""volume_object = models.Volumes.objects.create(
			comic_name=comic_object,
			volume_title="Volume Name",
			vol_number=1,
			date_published=datetime.date.today()
		)

		chapter_object = models.Chapters.objects.create(
			volume=volume_object,
			chapter_title="Chapter Name 1",
			chapter_number=1,
		)
		models.Pages.objects.create(
			chapter=chapter_object,
			page_number=1,
			page_img=self.a_simple_file
		)

		models.Personnel.objects.create(
			full_name="name 1",
			phone_number=521615,
			email_address="name@email.com",
			role_at_creative_cortex="founder",
			person_img_200_by_260=self.a_simple_file
		)"""



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
			comic_img_200_by_260=self.a_simple_file
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
			comic_img_200_by_260=a_simple_file
		)
		volume_object = models.Volumes.objects.create(
			comic_name=comic_object,
			volume_title="title",
			vol_number=-1,
			date_published=datetime.date.today()
		)

		"""Here we need to test the volume object does not exist"""
		"""And instead that an error is raised"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

"""
class WebNavigationTest(SimpleTestCase):


	def setUp(self):
		self.driver = webdriver.Safari()
		self.driver.get('http://127.0.0.1:8000/')
		time.sleep(1)

	def tearDown(self):
		self.driver.close()


	def testNavigationToHomepage(self):

		link = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(By.CLASS_NAME, "hamburger"))
		ActionChains(self.driver) \
			.click(link) \
			.perform()

		time.sleep(1)

		link_2 = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(By.CLASS_NAME, "homepage"))
		ActionChains(self.driver) \
			.click(link_2) \
			.perform()

		time.sleep(1)

		title = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(By.CLASS_NAME, "cc_text"))
		self.assertInHTML("CREATIVE CORTEX", title.text)

	def testNavigationToComics(self):
		link = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(By.CLASS_NAME, "hamburger"))
		ActionChains(self.driver) \
			.click(link) \
			.perform()

		time.sleep(1)

		link_2 = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(By.CLASS_NAME, "comics"))
		ActionChains(self.driver) \
			.click(link_2) \
			.perform()

		time.sleep(1)

		title = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(By.CLASS_NAME, "Title"))
		self.assertInHTML("Comics", title.text)

	def testNavigationToGallery(self):
		link = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(By.CLASS_NAME, "hamburger"))
		ActionChains(self.driver) \
			.click(link) \
			.perform()

		time.sleep(1)

		link_2 = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(By.CLASS_NAME, "gallery"))
		ActionChains(self.driver) \
			.click(link_2) \
			.perform()

		time.sleep(1)

		title = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(By.CLASS_NAME, "Title"))
		self.assertInHTML("Gallery", title.text)


	def testNavigationToLinks(self):


		link = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(By.CLASS_NAME, "hamburger"))
		ActionChains(self.driver) \
			.click(link) \
			.perform()

		time.sleep(1)

		hyperlink = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(By.CLASS_NAME,
									 "links"))
		self.driver.execute_script("return arguments[0].scrollIntoView();",
								   hyperlink)

		time.sleep(1)

		ActionChains(self.driver) \
			.move_to_element(hyperlink) \
			.perform()

		time.sleep(1)

		ActionChains(self.driver) \
			.click(hyperlink) \
			.perform()

		time.sleep(1)

		title = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(By.CLASS_NAME, "Title"))
		self.assertInHTML("Links", title.text)


	def testNavigationToAboutUs(self):
		link = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(By.CLASS_NAME, "hamburger"))
		ActionChains(self.driver) \
			.click(link) \
			.perform()

		time.sleep(1)

		hyperlink = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(
				By.CLASS_NAME,
				"about_us"
			)
		)

		self.driver.execute_script(
			"return arguments[0].scrollIntoView();",
			hyperlink
		)

		time.sleep(1)

		ActionChains(self.driver) \
			.move_to_element(hyperlink) \
			.perform()

		time.sleep(1)

		ActionChains(self.driver) \
			.click(hyperlink) \
			.perform()

		time.sleep(1)

		title = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(By.CLASS_NAME, "Title"))
		self.assertInHTML("About Us", title.text)

	def testNavigationToPages(self):

		link = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(By.CLASS_NAME, "hamburger"))
		ActionChains(self.driver) \
			.click(link) \
			.perform()

		time.sleep(1)

		link_2 = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(By.CLASS_NAME, "comics"))
		ActionChains(self.driver) \
			.click(link_2) \
			.perform()

		time.sleep(1)

		link_3 = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(By.CLASS_NAME, "c_pl_img"))
		ActionChains(self.driver) \
			.click(link_3) \
			.perform()

		time.sleep(1)

		link_4 = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(By.LINK_TEXT, "chapter: 1"))

		self.driver.execute_script(
			"return arguments[0].scrollIntoView();",
			link_4
		)

		time.sleep(1)

		ActionChains(self.driver) \
			.click(link_4) \
			.perform()

		time.sleep(1)

		button = WebDriverWait(self.driver, timeout=5).until(
			lambda d: d.find_element(
				By.CLASS_NAME,
				"b_2_ch_text"
			)
		)

		self.assertInHTML("Back To Chapters", button)
"""


class formInputTest(SimpleTestCase):

		def test_form_success(self):
			form = forms.NameForm(data={
				'your_name': 'Alice',
				'email_address': 'Alice@gmail.com',
				'subject': 'Hi I Would Like To Inquire About This And That'
			})

			self.assertTrue(form.is_valid())


		def test_form_no_email_provided(self):
			form = forms.NameForm(data={
				'your_name': 'Alice',
				'email_address': 'Alice',
				'subject': 'Hi I Would Like To Inquire About This And That'
			})

			self.assertFalse(form.is_valid())

		def test_form_no_email_provided_for_errors(self):
			form = forms.NameForm(data={
				'your_name': 'Alice',
				'email_address': 'Alice',
				'subject': 'Hi I Would Like To Inquire About This And That'
			})

			self.assertFalse(form.is_valid())

		def test_form_subject_too_long(self):
			form = forms.NameForm(data={
				'your_name': 'Alice',
				'email_address': 'Alice@gmail.com',
				'subject': "Hi I Would Like To Inquire About This And That, "
						   "Hi I Would Like To Inquire About This And That, "
						   "Hi I Would Like To Inquire About This And That , "
						   "Hi I Would Like To Inquire About This And That"
			})

			self.assertFalse(form.is_valid())

		def test_form_subject_too_long_for_errors(self):
			form = forms.NameForm(data={
				'your_name': 'Alice',
				'email_address': 'Alice@gmail.com',
				'subject': "Hi I Would Like To Inquire About This And That, "
						   "Hi I Would Like To Inquire About This And That, "
						   "Hi I Would Like To Inquire About This And That , "
						   "Hi I Would Like To Inquire About This And That"
			})


			self.assertIn("Ensure this value has at most 100 characters", str(form.errors))

		def test_form_subject_too_short_for_errors(self):
			form = forms.NameForm(data={
				'your_name': 'Alice',
				'email_address': 'Alice@gmail.com',
				'subject': "Hi"
			})
			errorMessage = 'Sorry but you must keep your message between 15 and 150 characters...'
			self.assertIn(errorMessage, str(form.errors))


		def test_form_subject_too_short_and_false_email_for_errors(self):
			form = forms.NameForm(data={
				'your_name': 'Alice',
				'email_address': 'Alicegmail.com',
				'subject': "Hi"
			})
			errorMessage_1 = 'Sorry but you must keep your message between 15 and 150 characters...'
			errorMessage_2 = 'Enter a valid email address.'

			self.assertIn(errorMessage_1, str(form.errors))
			self.assertIn(errorMessage_2, str(form.errors))


		def test_form_subject_for_open_script_errors(self):
			form = forms.NameForm(data={
				'your_name': 'Alice',
				'email_address': 'Alice@gmail.com',
				'subject': "Hi<script>myNameIsQuentin"
			})
			errorMessage_1 = 'An error has occurred'

			self.assertIn(errorMessage_1, str(form.errors))

		def test_form_subject_for_close_script_errors(self):
			form = forms.NameForm(data={
				'your_name': 'Alice',
				'email_address': 'Alice@gmail.com',
				'subject': "Hi</script>myNameIsQuentin"
			})
			errorMessage_1 = 'An error has occurred'

			print(forms.errors)
			print(forms.errors)
			print(forms.errors)
			self.assertIn(errorMessage_1, str(form.errors))


		def test_form_no_data(self):
			form = forms.NameForm(data={})

			self.assertFalse(form.is_valid())
			self.assertEquals(len(form.errors), 3)

