from django.test import SimpleTestCase
from . import forms


class formInputTest(SimpleTestCase):

	def test_form_success(self):
		form = forms.Name_Form(data={
			'your_name': 'Alice',
			'email_address': 'Alice@gmail.com',
			'subject': 'Hi I Would Like To Inquire About This And That'
		})

		self.assertTrue(form.is_valid())

	def test_form_no_email_provided(self):
		form = forms.Name_Form(data={
			'your_name': 'Alice',
			'email_address': 'Alice',
			'subject': 'Hi I Would Like To Inquire About This And That'
		})

		self.assertFalse(form.is_valid())

	def test_form_no_email_provided_for_errors(self):
		form = forms.Name_Form(data={
			'your_name': 'Alice',
			'email_address': 'Alice',
			'subject': 'Hi I Would Like To Inquire About This And That'
		})

		self.assertFalse(form.is_valid())

	def test_form_subject_too_long(self):
		form = forms.Name_Form(data={
			'your_name': 'Alice',
			'email_address': 'Alice@gmail.com',
			'subject': "Hi I Would Like To Inquire About This And That, "
			"Hi I Would Like To Inquire About This And That, "
			"Hi I Would Like To Inquire About This And That , "
			"Hi I Would Like To Inquire About This And That"
		})

		self.assertFalse(form.is_valid())

	def test_form_subject_too_long_for_errors(self):
		form = forms.Name_Form(data={
			'your_name': 'Alice',
			'email_address': 'Alice@gmail.com',
			'subject': "Hi I Would Like To Inquire About This And That, "
			"Hi I Would Like To Inquire About This And That, "
			"Hi I Would Like To Inquire About This And That , "
			"Hi I Would Like To Inquire About This And That"
		})

		self.assertIn(
			"Ensure this value has at most 100 characters",
			str(form.errors)
		)

	def test_form_subject_too_short_for_errors(self):
		form = forms.Name_Form(data={
			'your_name': 'Alice',
			'email_address': 'Alice@gmail.com',
			'subject': "Hi"
		})
		errorMessage = \
			'Sorry but you must keep your message ' \
			'between 15 and 150 characters...'
		self.assertIn(errorMessage, str(form.errors))


	def test_form_subject_too_short_and_false_email_for_errors(self):
		form = forms.Name_Form(data={
			'your_name': 'Alice',
			'email_address': 'Alicegmail.com',
			'subject': "Hi"
		})
		errorMessage_1 = 'Sorry but you must keep your message ' \
						 'between 15 and 150 characters...'
		errorMessage_2 = 'Enter a valid email address.'

		self.assertIn(errorMessage_1, str(form.errors))
		self.assertIn(errorMessage_2, str(form.errors))


	def test_form_subject_for_open_script_errors(self):
		form = forms.Name_Form(data={
			'your_name': 'Alice',
			'email_address': 'Alice@gmail.com',
			'subject': "Hi<script>myNameIsQuentin"
		})
		errorMessage_1 = 'An error has occurred'

		self.assertIn(errorMessage_1, str(form.errors))

	def test_form_subject_for_close_script_errors(self):
		form = forms.Name_Form(data={
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
		form = forms.Name_Form(data={})

		self.assertFalse(form.is_valid())
		self.assertEquals(len(form.errors), 3)


if __name__ == "__main__":
	unittest.main()
