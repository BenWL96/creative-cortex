from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class Name_Form(forms.Form):
	your_name = forms.CharField(label='Your name', max_length=25)
	email_address = forms.EmailField(label='Your email', max_length=50)
	subject = forms.CharField(label='Subject', max_length=100)

	def clean_email_address(self):
		data = self.cleaned_data['email_address']
		js_error = "An error has occurred"

		try:
			validate_email(data)
		except ValidationError as e:
			raise e
		else:
			if '<script>' in str(data) or '</script>' in str(data):
				raise ValidationError(js_error)
			else:
				return data

	def clean_subject(self):
		data = self.cleaned_data['subject']
		lengthError = "Sorry but you must keep your message between 15 and 500 characters..."
		js_error = "An error has occurred"

		if 15 <= len(str(data)) <= 500:
			return data
		elif '<script>' in str(data) or '</script>' in str(data):
			raise ValidationError(js_error)
		else:
			raise ValidationError(lengthError)

	def clean_your_name(self):
		data = self.cleaned_data['your_name']
		js_error = "An error has occurred"

		if '<script>' in str(data) or '</script>' in str(data):
			raise ValidationError(js_error)
		else:
			return data
