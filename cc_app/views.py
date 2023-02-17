from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from . import models, utils


def Landing_Page(request):
	carousel_img_objects = models.Landing_Page_Images.objects.all().order_by(
		"landing_page_img_carousel_placement_number"
	)
	context = {'carousel_img_objects': carousel_img_objects}
	return render(request, 'cc_app/landing_page.html', context)


def Comics(request):

	comics_page_obj = models.Web_Pages.objects.filter(page_name="Comics")

	if len(comics_page_obj) > 0:
		# If there is no img_url, then null will be passed I think
		header_img_url = comics_page_obj[0].header_img_url
	else:
		header_img_url = False

	comics = models.Comics.objects.filter(display_comic=True)

	context = {
		'comics': comics,
		'header_img_url': header_img_url
	}
	return render(request, 'cc_app/comics.html', context)


def Comic_Detail(request, comic_param):

	try:
		comic = models.Comics.objects.get(slug=comic_param, display_comic=True)

	except models.Comics.DoesNotExist:
		print("comic with name '" + comic_param + "' was not found")
		return redirect('comics')

	comic_personnel_related = models.Comic_Personnel.objects.select_related(
		'comic_id').filter(comic_id=comic)

	# only show volumes which have chapters
	volumes_related_to_comic_param = models.Volumes.objects.select_related(
		'comic_name').filter(comic_name=comic)

	list_volumes_with_chapters =\
		utils.take_volumes_of_comic_return_list_volumes_with_chapters(volumes_related_to_comic_param)
	volumes_with_chapters_and_pages = utils.take_volumes_with_chap_return_list_volumes_that_have_chapters_and_pages(list_volumes_with_chapters)

	# HEADER IMG
	header_img_url = utils.fetch_comic_detail_page_return_img_url()

	volumes_related_count = len(volumes_with_chapters_and_pages)

	if volumes_related_count > 0:

		# Here we find all the chapters related to the volumes

		print("comic found and volumes found")
		chapters_related = utils.return_chapters_related_to_volumes_queryset(
			volumes_related_to_comic_param
		)

		# Find pages related to chapters. if no pages in chapter,
		# then don't append chapter to the list of chapter objects.

		chapters = utils.return_list_chapters_with_pages(chapters_related)

		# nested author logic in template such that if
		context = {
			'comic': comic,
			'volumes': volumes_with_chapters_and_pages,
			'chapters': chapters,
			'comic_personnel_related': comic_personnel_related,
			'header_img_url': header_img_url
		}

	else:

		print("comic found but volumes not found")
		context = {
			'comic': comic,
			'comic_personnel_related': comic_personnel_related,
			'header_img_url': header_img_url
		}

	return render(request, "cc_app/comic_detail.html", context)


def Pages(request, comic_param, volume_param, chapter_param, page_param):

	chapter_volume_comic_objects =\
		utils.find_chapter_with_all_pages_from_params_or_redirect(
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

	# Only gets this far if all of the pages are found.

	# This page_related_count logic is used to determine
	# The final page count, which then allows for page navigation

	pages_related = models.Pages.objects.select_related(
		'chapter').filter(chapter=chapter)

	last_page_object = pages_related.last()
	last_page_number = last_page_object.page_id

	param_equal_to_one_boolean = page_param == 1
	param_equals_final_page_id_boolean = page_param == last_page_number

	if param_equal_to_one_boolean is True:
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
	elif param_equals_final_page_id_boolean is True:
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

	featured_videos =\
		models.Featured_Youtube_videos.objects.all().order_by("video_ordering")

	page_text_content, header_img_url =\
		utils.fetch_links_page_return_content_and_img_url()

	context = utils.Pass_Links_Text_Return_Context(
		featured_videos,
		page_text_content,
		header_img_url
	)
	print(page_text_content)

	return render(request, 'cc_app/links.html', context)


def About_Us(request):

	form = utils.form_logic_about_us(request)
	# This needs to be named something else to make it more clear...
	if type(form) == bool:
		return HttpResponseRedirect('/about-us/')

	list_personnel = utils.assign_personnel_objects_even_boolean_return_list()

	page_text_content, header_img_url =\
		utils.fetch_about_us_page_return_content_and_img_url()

	context = utils.Pass_About_Us_Text_Return_Context(
		form, list_personnel, page_text_content, header_img_url
	)

	return render(request, 'cc_app/about_us.html', context)


def Gallery(request):

	header_img_url = utils.fetch_gallery_page_return_img_url()

	ordered_gallery_img_objects = models.Gallery_images.objects.all().order_by(
		"gallery_img_placement_number"
	)
	context = {
		'gallery_images': ordered_gallery_img_objects,
		'header_img_url': header_img_url
	}

	return render(request, 'cc_app/gallery.html', context)


def error404(request, exception):
	return render(request, 'cc_app/error_404.html', status=404)


def error500(request):
	return render(request, 'cc_app/error_500.html', status=500)
