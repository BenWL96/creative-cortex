import unittest
from django.urls import reverse, resolve
from cc_app import views

class testPatternNameResolveToView(unittest.TestCase):

	def test_Landing_Page_View(self):
		url = reverse('landing_page')
		self.assertEqual(resolve(url).func, views.Landing_Page)
