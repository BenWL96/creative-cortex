from . import models, forms
from django.shortcuts import redirect
import re

SLUG_REGEX = re.compile('^[-\w]+$')

def check_type_param_comic_slug_boolean(comic_param):

	try:
		if SLUG_REGEX.match(comic_param):
			return True
	except TypeError as e:
		print(e)
		return False


def check_type_volume_param_boolean(volume_param):

	if type(volume_param) == int:
		return True
	return False

def check_type_chapter_param_boolean(chapter_param):

	if type(chapter_param) == int:
		return True
	return False

def check_type_page_param_boolean(page_param):

	if type(page_param) == int:
		return True
	return False


def find_chapter_with_all_pages_from_params_or_redirect(
		comic_param,
		volume_param,
		chapter_param,
		page_param
):

	# We can try to condense this down into a single database query.
	type_check_comic_slug_passed = check_type_param_comic_slug_boolean(
		comic_param,
	)
	type_check_volume_param_passed = check_type_volume_param_boolean(
		volume_param,
	)

	type_check_chapter_param_passed = check_type_chapter_param_boolean(
		chapter_param,
	)
	type_check_page_param_passed = check_type_page_param_boolean(
		page_param,
	)

	if (
			type_check_comic_slug_passed == False and
			type_check_volume_param_passed == False and
			type_check_chapter_param_passed == False and
			type_check_page_param_passed == False):

		return redirect('landing_page')

	#the redirects here won't work becuase we are assuming these redirects are
	#legitimate

	try:

		comic = models.Comics.objects.get(slug=comic_param)
		print("comic successfully found")

	except models.Comics.DoesNotExist:

		print("could not find comic called " + comic_param + ".")
		return redirect('comics')

	# if related volume object does not exist redirect

	try:

		volume = models.Volumes.objects.select_related('comic_name').get(
			vol_number=volume_param, comic_name=comic)
		print("volume successfully found")

	except:
		print("volume " + str(volume_param) + " doesn't exist to comic " + comic_param + ".")
		return redirect('comics')

	try:

		chapter = models.Chapters.objects.select_related('volume').get(
			volume=volume,
			chapter_number=chapter_param,
			all_pages_exist_enable_displaying=True
		)
		print("chapter successfully found that has all its pages")

	except:

		print("Chapter " + str(chapter_param) + " doesn't exist to volume " + str(volume_param) + " of " + comic_param + ".")
		print("Or doesn't have all its pages.")
		return redirect('comics')

	try:

		page = models.Pages.objects.select_related('chapter').get(
			chapter=chapter,
			page_number=page_param,
		)
		print("chapter successfully found that has all its pages")

	except:

		print("Page " + str(page_param) + " doesn't exist to chapter " + chapter_param)
		print("of volume" + str(volume_param) + " of " + comic_param + ".")
		return redirect('comics')


	print("how did we get this far")
	return [chapter, volume, comic, page]


def return_chapters_related_to_volumes_queryset(volumes_related):
	chapters_related = list()

	for volume in volumes_related.iterator():
		# [vol1, vol2]
		chapters = models.Chapters.objects.select_related('volume').filter(
			volume=volume)
		for chapter in chapters:
			chapters_related.append(chapter)

	return chapters_related


def return_list_chapters_with_pages(chapters_related):
	chapters = list()

	for chapter in chapters_related:
		pages_related = models.Pages.objects.select_related(
			'chapter').filter(chapter=chapter)
		if pages_related.count() > 0:
			chapters.append(chapter)

	return chapters

def take_volumes_of_comic_return_list_volumes_with_chapters(volumes_related_to_comic_param):

	volumes_with_chapters = list()

	for volume in volumes_related_to_comic_param:

		chapters_related = list(models.Chapters.objects.select_related(
			'volume').filter(volume=volume))

		if len(chapters_related) > 0:
			volumes_with_chapters.append(volume)

	return volumes_with_chapters


def take_volumes_with_chap_return_list_volumes_that_have_chapters_and_pages(
		list_volumes_with_chapters
):
	volumes_with_chapters_and_pages = list()


	for volume_with_chapter in list_volumes_with_chapters:

			chapters_of_volumes_with_chapters = list(
				models.Chapters.objects.select_related(
					'volume').filter(volume=volume_with_chapter)
			)

			print(chapters_of_volumes_with_chapters)
			print(len(chapters_of_volumes_with_chapters))


			if len(chapters_of_volumes_with_chapters) > 0:
				#for every chapter in every volume
				#We are investigating the pages of the chapters which belong to volume_with_chapter

				for chapter_of_volumes_with_chapters in chapters_of_volumes_with_chapters:
					pages_of_chapters_of_volumes_with_chapters_with_pages = list(
						models.Pages.objects.select_related(
							'chapter').filter(chapter=chapter_of_volumes_with_chapters)
					)

					if len(pages_of_chapters_of_volumes_with_chapters_with_pages) > 0:

						if volume_with_chapter not in volumes_with_chapters_and_pages:
							volumes_with_chapters_and_pages.append(volume_with_chapter)


	return volumes_with_chapters_and_pages



def assign_personnel_objects_even_boolean_return_list():

	list_personnel = list()

	personnel = models.Personnel.objects.all()
	if len(personnel) > 0:
		for person in personnel.iterator():

			if person.personnel_id % 2 == 0:
				print(str(person.personnel_id) + " is an even number")
				person.even = 'true'
			else:
				print(str(person.personnel_id) + " is an odd number")
				person.even = 'false'

			list_personnel.append(person)

	return list_personnel


def Pass_About_Us_Text_Return_Context(form, list_personnel, page_text_content, header_img_url):

	if page_text_content.count() == 1:
		context = {
			'form': form,
			'personnel': list_personnel,
			'header_img_url': header_img_url,
			'page_text_content_1': page_text_content[0]
		}

	elif page_text_content.count() == 2:
		context = {
			'form': form,
			'personnel': list_personnel,
			'header_img_url': header_img_url,
			'page_text_content_1': page_text_content[0],
			'page_text_content_2': page_text_content[1]
		}
	elif page_text_content.count() == 3:
		context = {
			'form': form,
			'personnel': list_personnel,
			'header_img_url': header_img_url,
			'page_text_content_1': page_text_content[0],
			'page_text_content_2': page_text_content[1],
			'page_text_content_3': page_text_content[2]
		}
	elif page_text_content.count() == 4:
		context = {
			'form': form,
			'personnel': list_personnel,
			'header_img_url': header_img_url,
			'page_text_content_1': page_text_content[0],
			'page_text_content_2': page_text_content[1],
			'page_text_content_3': page_text_content[2],
			'page_text_content_4': page_text_content[3]
		}
	elif page_text_content.count() == 5:
		context = {
			'form': form,
			'personnel': list_personnel,
			'header_img_url': header_img_url,
			'page_text_content_1': page_text_content[0],
			'page_text_content_2': page_text_content[1],
			'page_text_content_3': page_text_content[2],
			'page_text_content_4': page_text_content[3],
			'page_text_content_5': page_text_content[4],
		}

	else:
		context = {
			'form': form,
			'personnel': list_personnel,
			'header_img_url': header_img_url,
		}

	return context



def Pass_Links_Text_Return_Context(featured_videos, page_text_content, header_img_url):

	if page_text_content.count() == 1:
		context = {
			'featured_videos': featured_videos,
			'header_img_url': header_img_url,
			'page_text_content_1': page_text_content[0]
		}

	elif page_text_content.count() == 2:
		context = {
			'featured_videos': featured_videos,
			'header_img_url': header_img_url,
			'page_text_content_1': page_text_content[0],
			'page_text_content_2': page_text_content[1]
		}
	elif page_text_content.count() == 3:
		context = {
			'featured_videos': featured_videos,
			'header_img_url': header_img_url,
			'page_text_content_1': page_text_content[0],
			'page_text_content_2': page_text_content[1],
			'page_text_content_3': page_text_content[2]
		}
	elif page_text_content.count() == 4:
		context = {
			'featured_videos': featured_videos,
			'header_img_url': header_img_url,
			'page_text_content_1': page_text_content[0],
			'page_text_content_2': page_text_content[1],
			'page_text_content_3': page_text_content[2],
			'page_text_content_4': page_text_content[3]
		}
	elif page_text_content.count() == 5:
		context = {
			'featured_videos': featured_videos,
			'header_img_url': header_img_url,
			'page_text_content_1': page_text_content[0],
			'page_text_content_2': page_text_content[1],
			'page_text_content_3': page_text_content[2],
			'page_text_content_4': page_text_content[3],
			'page_text_content_5': page_text_content[4],
		}

	else:
		context = {
			'featured_videos': featured_videos,
			'header_img_url': header_img_url
		}

	return context

def fetch_about_us_page_return_content_and_img_url():
	about_page_obj = models.Web_Pages.objects.filter(page_name="About Us")

	if len(about_page_obj) > 0:
		page_text_content = about_page_obj[
			0].web_page_text_content_set.all().order_by('text_content_ordering')
		# If there is no img_url, then null will be passed I think
		header_img_url = about_page_obj[0].header_img_url
	else:
		print("There are no about page objects")

		# This should be a boolean instead of "placeholder"
		page_text_content = "Placeholder"
		header_img_url = False

	return page_text_content, header_img_url


def fetch_gallery_page_return_content_and_img_url():

	gallery_page_obj = models.Web_Pages.objects.filter(page_name="Gallery")

	if len(gallery_page_obj) > 0:
		# If there is no img_url, then null will be passed I think
		header_img_url = gallery_page_obj[0].header_img_url
	else:
		header_img_url = False

	return header_img_url


def form_logic_about_us(request):
	if request.method == 'POST':

		form = forms.Name_Form(request.POST)

		if form.is_valid():

			clean_form = form.cleaned_data

			# This finally takes the information from that dictionary and then
			# accesses the data within the fields.

			# This also completes all the custom validation.
			your_name = clean_form['your_name']
			your_email = clean_form['email_address']
			your_subject = clean_form['subject']

			models.Inquiries.objects.create(
				name=your_name,
				email=your_email,
				inquiry=your_subject
			)

			print("inquiry has been added to the database")

			# Redirect To ThankYouPage
			return True

		else:
			# form is not valid and so we must render error messages
			form = forms.Name_Form(request.POST)
	else:

		form = forms.Name_Form()

	return form