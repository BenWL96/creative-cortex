from django.test import TestCase
from . import models, utils, forms
from phonenumber_field.phonenumber import PhoneNumber
import datetime, tempfile
from django.http import HttpResponseRedirect


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

		chapters_related = utils.return_chapters_related_to_volumes_queryset(
			volumes_related
		)
		chapters_related_count = len(chapters_related)
		self.assertEqual(chapters_related_count, 2)

	def test_type_param_comic_slug_boolean_false(self):
		comic_param = 1512
		type_check_passed = utils.check_type_param_comic_slug_boolean(
			comic_param
		)
		self.assertEqual(type_check_passed, False)

	def test_type_param_comic_slug_boolean_true(self):
		comic_param = 'comic-123'
		type_check_passed = utils.check_type_param_comic_slug_boolean(
			comic_param
		)
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
		type_check_passed = utils.check_type_chapter_param_boolean(
			chapter_param
		)
		self.assertEqual(type_check_passed, False)

	def test_check_type_chapter_param_boolean_true(self):
		chapter_param = 1512
		type_check_passed = utils.check_type_chapter_param_boolean(
			chapter_param
		)
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

		comic_param = "comic_1"
		volume_param = 1
		chapter_param = 1
		page_param = 1

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

		personnel_list =\
			utils.assign_personnel_objects_even_boolean_return_list()
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

		personnel_list =\
			utils.assign_personnel_objects_even_boolean_return_list()

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

		page_text_content, header_img_url =\
			utils.fetch_links_page_return_content_and_img_url()

		context = utils.Pass_Links_Text_Return_Context(
			featured_video,
			page_text_content,
			header_img_url
		)

		self.assertEqual(len(context), 4)

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

		page_text_content, header_img_url =\
			utils.fetch_about_us_page_return_content_and_img_url()
		personnel = models.Personnel.objects.all()
		form = forms.Name_Form
		context = utils.Pass_About_Us_Text_Return_Context(
			form,
			personnel,
			page_text_content,
			header_img_url
		)

		self.assertEqual(len(context), 5)

	def test_about_us_page_return_content_and_img_url_no_obj(self):
		page_text_content, header_img_url =\
			utils.fetch_about_us_page_return_content_and_img_url()
		self.assertEqual(header_img_url, False)
		self.assertEqual(page_text_content, "No text")

	def test_fetch_gallery_page_return_img_url_no_obj(self):
		img_url = utils.fetch_gallery_page_return_img_url()
		self.assertEqual(img_url, False)

	def test_fetch_links_page_return_content_and_img_url_no_obj(self):
		page_text_content, header_img_url =\
			utils.fetch_links_page_return_content_and_img_url()
		self.assertEqual(header_img_url, False)
		self.assertEqual(page_text_content, "No text")

	def test_fetch_comic_detail_page_return_img_url_no_obj(self):
		img_url = utils.fetch_comic_detail_page_return_img_url()
		self.assertEqual(img_url, False)

	def test_about_us_page_return_content_and_img_url_with_obj(self):

		page_name = models.Web_Pages.objects.create(
			page_name="About Us"
		)
		models.Web_Page_Text_Content.objects.create(
			page_name=page_name,
			text_content_ordering=1,
			text_content="ipsum"
		)
		page_text_content, header_img_url =\
			utils.fetch_about_us_page_return_content_and_img_url()
		self.assertNotEqual(header_img_url, False)
		self.assertNotEqual(page_text_content, "No text")

	def test_fetch_gallery_page_return_img_url_with_obj(self):
		models.Web_Pages.objects.create(
			page_name="Gallery"
		)
		img_url = utils.fetch_gallery_page_return_img_url()
		self.assertNotEqual(img_url, False)

	def test_fetch_links_page_return_content_and_img_url_with_obj(self):
		page_name = models.Web_Pages.objects.create(
			page_name="Links"
		)
		models.Web_Page_Text_Content.objects.create(
			page_name=page_name,
			text_content_ordering=1,
			text_content="ipsum"
		)
		page_text_content, header_img_url =\
			utils.fetch_links_page_return_content_and_img_url()
		self.assertNotEqual(header_img_url, False)
		self.assertNotEqual(page_text_content, "No text")

	def test_fetch_comic_detail_page_return_img_url_no_obj(self):
		models.Web_Pages.objects.create(
			page_name="Comic Detail"
		)
		img_url = utils.fetch_comic_detail_page_return_img_url()
		self.assertNotEqual(img_url, False)
