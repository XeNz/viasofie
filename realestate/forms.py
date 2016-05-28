from django import forms
# from haystack.forms import SearchForm
from django.contrib.auth.models import User
from .models import *
from nocaptcha_recaptcha.fields import NoReCaptchaField



class FeedbackForm(forms.Form):
    from_email = forms.EmailField(label="E-mail")
    subject = forms.CharField(label="Onderwerp")
    message = forms.CharField(label="Vraag",widget=forms.Textarea)
    captcha = NoReCaptchaField()
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ShareForm(forms.Form):
    from_email = forms.EmailField(label="E-mail")
    subject = forms.CharField(label="Onderwerp")
    message = forms.CharField(label="Bericht",widget=forms.Textarea)
    captcha = NoReCaptchaField()
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


# class PropertiesSearchForm(SearchForm):
#     def __init__(self, *args, **kwargs):
#         super(PropertiesSearchForm, self).__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'

#     class Meta:
#         model = Property



class UpdateAccountInformation(forms.ModelForm):

    #TODO: email?
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class IndexSearchForm(forms.Form):
    listing_type_choices = forms.ChoiceField(choices=Property.LISTING_TYPE_CHOICES,widget=forms.Select(attrs={'class': 'elselect'}))
    province_choices = forms.ModelChoiceField(queryset=Location.objects.none(),widget=forms.Select(attrs={'id': 'select_province', 'class': 'elselect'}),required = True)
    #TODO: NTH filter per provincie
    borough_choices = forms.ModelChoiceField(queryset=Location.objects.none(),widget=forms.Select(attrs={'class': 'elselect'}))
    propertytype = forms.ModelChoiceField(queryset=PropertyType.objects.none(),widget=forms.Select(attrs={'class': 'elselect'}))
    bedrooms = forms.ChoiceField(choices=((str(x), x) for x in range(1,10)),widget=forms.Select(attrs={'class': 'elselect'}))
    bathrooms = forms.ChoiceField(choices=((str(x), x) for x in range(1,10)),widget=forms.Select(attrs={'class': 'elselect'}))
    surfacearea = forms.ChoiceField(choices=((str(x), x) for x in xrange(50,210,10)),widget=forms.Select(attrs={'class': 'elselect'}))
    minprice = forms.CharField(widget=forms.TextInput(attrs={'class': 'eltextinput','type':'number'}),required = True,)
    maxprice = forms.CharField(widget=forms.TextInput(attrs={'class': 'eltextinput','type':'number'}),required = True,)


