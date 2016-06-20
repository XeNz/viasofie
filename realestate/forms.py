from django import forms
# from haystack.forms import SearchForm
from django.contrib.auth.models import User
from .models import *
from nocaptcha_recaptcha.fields import NoReCaptchaField
from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_integer


class FeedbackForm(forms.Form):
    name = forms.CharField(label="Naam")
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
        super(ShareForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class EbookRequestForm(forms.Form):
    from_email = forms.EmailField(label="E-mail")
    ebooks = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple, choices=Ebook.objects.all)
    captcha = NoReCaptchaField()
    def __init__(self, *args, **kwargs):
        super(EbookRequestForm, self).__init__(*args, **kwargs)
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
    first_name = forms.CharField(label=_('First Name'), widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label=_('Last Name') , widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(label=_('Email adress') , widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = ClientUser
        fields = ['first_name', 'last_name', 'email']

class ReferenceSearchForm(forms.Form):
    property_id = forms.CharField(label=_('Reference id'),widget=forms.TextInput(attrs={'class':'eltextinput', 'type':'number'}),required = True,)

    class Meta:
        model = Property
        fields = ['id',]
    def clean(self):
        if self.cleaned_data['property_id'] is not None or self.cleaned_data['property_id'] != '' :
              return super().clean()
        raise ValidationError_('no correct reference number')

class IndexSearchForm(forms.Form):
    listing_type_choices = forms.ChoiceField(choices=Property.LISTING_TYPE_CHOICES,widget=forms.Select(attrs={'class': 'elselect'}),required=False)
    # province_choices = forms.ModelChoiceField(queryset=Location.objects.none(),widget=forms.Select(attrs={'id': 'select_province', 'class': 'elselect'}),required = True)
    #TODO: NTH filter per provincie
    borough_choices = forms.ModelChoiceField(queryset=Location.objects.values_list('gemeente',flat=True).distinct().order_by('gemeente'),widget=forms.Select(attrs={'class': 'elselect'}))
    propertytype = forms.ModelChoiceField(queryset=PropertyType.objects.values_list('name',flat=True).distinct(),widget=forms.Select(attrs={'class': 'elselect'}))
    bedrooms = forms.ChoiceField(choices=((str(x), x) for x in range(1,10)),widget=forms.Select(attrs={'class': 'elselect'}))
    bathrooms = forms.ChoiceField(choices=((str(x), x) for x in range(1,10)),widget=forms.Select(attrs={'class': 'elselect'}))
    surfacearea = forms.ChoiceField(choices=((str(x), x) for x in range(50,210,10)),widget=forms.Select(attrs={'class': 'elselect'}))
    minprice = forms.CharField(widget=forms.TextInput(attrs={'class': 'eltextinput','type':'number'}),required = True,)
    maxprice = forms.CharField(widget=forms.TextInput(attrs={'class': 'eltextinput','type':'number'}),required = True,)


class PropertyAdminForm(forms.ModelForm):
    title_text = forms.CharField(label=_('Property|title_text'))
    description_text = forms.CharField(label=_('Property|description_text'), widget=forms.Textarea)
    street_text = forms.CharField(label=_('Property|street_text'))
    house_number_text = forms.CharField(label=_('Property|house_number_text'))
    postcodes = Location.objects.values_list('postcode', flat=True).distinct().order_by('postcode')
    postcodes_choices = [('', 'None')] + [(postcode, postcode) for postcode in postcodes]
    postal_code_text = forms.ChoiceField(postcodes_choices,
                                required=True, widget=forms.Select(),label=_('Property|postal_code_text'))
    gemeentes = Location.objects.values_list('gemeente', flat=True).distinct()
    gemeentes_choices = [('', 'None')] + [(gemeente, gemeente) for gemeente in gemeentes]
    city_text = forms.ChoiceField(gemeentes_choices,
                                required=True, widget=forms.Select(),label=_('Property|city_text'))
    country_text = forms.CharField(label=_('Property|country_text'))
    constructiondate = forms.DateField(label=_('Property|constructiondate'), widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
    sellingprice = forms.IntegerField(label=_('Property|sellingprice'))
    visible_to_public = forms.BooleanField(required=False,label=_('Property|visible_to_public'))
    featured = forms.BooleanField(required=False,label=_('Property|featured'))
    pub_date = forms.DateTimeField(label=_('Property|datepublished'))
    surface_area_text = forms.IntegerField(label=_('Property|surface_area_text'))
    bathrooms_text = forms.IntegerField(label=_('Property|bathrooms_text'))
    bedrooms_text = forms.IntegerField(label=_('Property|bedrooms_text'))

    class Meta:
        model = Property
        fields = '__all__'


