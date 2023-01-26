from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class NameForm(forms.Form):
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
		lengthError = "Sorry but you must keep your message between 15 and 150 characters..."
		js_error = "An error has occurred"

		if 15 <= len(str(data)) <= 150:
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



#phone Number Validation Code
"""
from django.core.validators import RegexValidator

regex_phone_number_validator = \
	RegexValidator(
		'^(?:(?:\(?(?:0(?:0|11)\)?[\s-]?\(?|\+)44\)?[\s-]?(?:\(?0\)?[\s-]?)?)|(?:\(?0))(?:(?:\d{5}\)?[\s-]?\d{4,5})|(?:\d{4}\)?[\s-]?(?:\d{5}|\d{3}[\s-]?\d{3}))|(?:\d{3}\)?[\s-]?\d{3}[\s-]?\d{3,4})|(?:\d{2}\)?[\s-]?\d{4}[\s-]?\d{4}))(?:[\s-]?(?:x|ext\.?|\#)\d{3,4})?$',
			message="please enter your phone number correctly")"""

# phone_number = forms.CharField(label='Phone Number', validators=[regex_phone_number_validator], max_length=11)


""""def clean_phone_number(self):
    data = self.cleaned_data['phone_number']
    if data == False:
        return "false"
    return data"""