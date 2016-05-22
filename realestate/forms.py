from django import forms
from haystack.forms import SearchForm
from django.contrib.auth.models import User
from .models import Property
from nocaptcha_recaptcha.fields import NoReCaptchaField


PRIJS = (
         ("0", "0"),
         ("50000", "50000"),
         ("100000", "100000"),
         ("200000", "200000"),
         ("300000", "300000"),
         ("400000", "400000"),
         ("500000", "500000"),
         )

class FeedbackForm(forms.Form):
    from_email = forms.EmailField(label="E-mail")
    subject = forms.CharField(label="Onderwerp")
    message = forms.CharField(label="Vraag",widget=forms.Textarea)
    captcha = NoReCaptchaField()
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class PropertiesSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        super(PropertiesSearchForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Property



class UpdateAccountInformation(forms.ModelForm):

    #TODO: email?
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


