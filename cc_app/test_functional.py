from django.test import SimpleTestCase
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class WebNavigationTest(SimpleTestCase):

	# These test will not work because the class names
	# have changed since writing these tests !

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


if __name__ == "__main__":
	unittest.main()
	