import unittest

from django.urls import resolve, reverse

from . import views


class testPatternNameResolveToView(unittest.TestCase):

	def test_Landing_Page_View(self):
		url = reverse('landing_page')
		self.assertEqual(resolve(url).func, views.Landing_Page)

	def test_Comics_View_No_Comics(self):
		url = reverse('comics')
		self.assertEqual(resolve(url).func, views.Comics)

	def test_Volumes_View_No_Comics(self):
		# If no comics exists go to landin pages
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


if __name__ == "__main__":
	unittest.main()
	pass
