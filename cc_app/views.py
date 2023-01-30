from django.shortcuts import render
from . import models, utils, forms
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect


def Landing_Page(request):
	carousel_img_objects = models.Landing_Page_Images.objects.all().order_by(
		"landing_page_img_carousel_placement_number"
	)
	context = {'carousel_img_objects': carousel_img_objects}
	return render(request, 'cc_app/landing_page.html', context)

def Comics(request):
	comics = models.Comics.objects.all()
	context = {'comics': comics}
	return render(request, 'cc_app/comics.html', context)

def Comic_Detail(request, comic_param):

	try:
		comic = models.Comics.objects.get(slug=comic_param)

	except models.Comics.DoesNotExist:
		print("comic with name '" + comic_param + "' was not found")
		return redirect('comics')

	comic_personnel_related = models.Comic_Personnel.objects.select_related(
		'comic_id').filter(comic_id=comic)

	# only show volumes which have chapters
	volumes_related_to_comic_param = models.Volumes.objects.select_related(
		'comic_name').filter(comic_name=comic)

	list_volumes_with_chapters = utils.take_volumes_of_comic_return_list_volumes_with_chapters(volumes_related_to_comic_param)
	volumes_with_chapters_and_pages = utils.take_volumes_with_chap_return_list_volumes_that_have_chapters_and_pages(list_volumes_with_chapters)


	volumes_related_count = len(volumes_with_chapters_and_pages)

	if volumes_related_count > 0:

		# Here we find all the chapters related to the volumes

		print("comic found and volumes found")
		chapters_related = utils.return_chapters_related_to_volumes_queryset(
			volumes_related_to_comic_param
		)

		# Find pages related to chapters. if no pages in chapter, then don't append chapter
		# To the list of chapter objects.

		chapters = utils.return_list_chapters_with_pages(chapters_related)

		# nested author logic in template such that if
		context = {
			'comic': comic,
			'volumes': volumes_with_chapters_and_pages,
			'chapters': chapters,
			'comic_personnel_related': comic_personnel_related
		}

	else:

		print("comic found but volumes not found")
		context = {
			'comic': comic,
			'comic_personnel_related': comic_personnel_related
		}

	return render(request, "cc_app/comic_detail.html", context)

#List view won't work because this is a detail view !!

def Pages(request, comic_param, volume_param, chapter_param, page_param):


	chapter_volume_comic_objects = utils.find_chapter_with_all_pages_from_params_or_redirect(
		comic_param,
		volume_param,
		chapter_param,
		page_param
	)

	if type(chapter_volume_comic_objects) != HttpResponseRedirect:
		chapter = chapter_volume_comic_objects[0]
		volume = chapter_volume_comic_objects[1]
		comic = chapter_volume_comic_objects[2]
		current_page_object = chapter_volume_comic_objects[3]
	else:
		redirect = chapter_volume_comic_objects
		return redirect

	#Only gets this far if all of the pages are found.
	#This can only be set by the admin user.

	#This page_related_count logic is used to determine
	#The final page count, which then allows for page navigation

	pages_related = models.Pages.objects.select_related(
		'chapter').filter(chapter=chapter)

	last_page_object = pages_related.last()
	last_page_number = last_page_object.page_id

	param_equal_to_one_boolean = page_param == 1
	param_equals_final_page_id_boolean = page_param == last_page_number

	if param_equal_to_one_boolean == True:
		next_page = page_param + 1

		context = {
			'comic': comic,
			'volume': volume,
			'chapter': chapter,
			'current_page_obj': current_page_object,
			'next_page_number': next_page,
			'next_page_exists': True,
			'previous_page_exists': False,
			'current_page_number': page_param
		}
	elif param_equals_final_page_id_boolean == True:
		previous_page = page_param - 1

		context = {
			'comic': comic,
			'volume': volume,
			'chapter': chapter,
			'current_page_obj': current_page_object,
			'previous_page_number': previous_page,
			'next_page_exists': False,
			'previous_page_exists': True,
			'current_page_number': page_param
		}

	else:

		next_page = page_param + 1
		previous_page = page_param - 1

		context = {
			'comic': comic,
			'volume': volume,
			'chapter': chapter,
			'current_page_obj': current_page_object,
			'next_page_number': next_page,
			'previous_page_number': previous_page,
			'next_page_exists': True,
			'previous_page_exists': True,
			'current_page_number': page_param
		}


	return render(request, 'cc_app/pages.html', context)

def Links(request):

	featured_videos = models.Featured_Youtube_videos.objects.all().order_by("video_ordering")
	links_page_obj = models.Web_Pages.objects.filter(page_name="Links")
	# page_text_content = models.Web_Page_Text_Content.objects.select_related('page_name')

	if len(links_page_obj) > 0:
		page_text_content = links_page_obj[0].web_page_text_content_set.all().order_by('text_content_ordering')
		header_img_url = links_page_obj[0]
	else:
		print("There is no text for the links page")
		page_text_content = "No text"

	context = utils.Pass_Links_Text_Return_Context(
		featured_videos,
		page_text_content,
		header_img_url
	)
	print(page_text_content)

	return render(request, 'cc_app/links.html', context)

def About_Us(request):

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
			return HttpResponseRedirect('/about-us/')

		else:
			# form is not valid and so we must render error messages
			form = forms.Name_Form(request.POST)
	else:

		form = forms.Name_Form()

	list_personnel = utils.assign_personnel_objects_even_boolean_return_list()

	about_page_obj = models.Web_Pages.objects.filter(page_name="About Us")

	if len(about_page_obj) > 0:
		page_text_content = about_page_obj[0].web_page_text_content_set.all().order_by('text_content_ordering')
		header_img_url = about_page_obj[0]
	else:
		print("There are no about page objects")
		page_text_content = "Placeholder"


	context = utils.Pass_About_Us_Text_Return_Context(
		form, list_personnel, page_text_content, header_img_url
	)

	return render(request, 'cc_app/about_us.html', context)


def Gallery(request):

	ordered_gallery_img_objects = models.Gallery_images.objects.all().order_by(
		"gallery_img_placement_number"
	)
	context = {'gallery_images': ordered_gallery_img_objects}

	return render(request, 'cc_app/gallery.html', context)



def error404(request, exception):
	return render(request, 'cc_app/error_404.html', status=404)


def error500(request):
	return render(request, 'cc_app/error_500.html', status=500)