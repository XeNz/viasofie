from django import forms
from haystack.forms import SearchForm
from django.contrib.auth.models import User

PRIJS = (
         ("0", "0"),
         (50000),
         (100000),
         (200000),
         (300000),
         (400000),
         (500000),
         )

class FeedbackForm(forms.Form):
    from_email = forms.EmailField(label="E-mail")
    subject = forms.CharField(label="Onderwerp")
    message = forms.CharField(label="Vraag",widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class PropertiesSearchForm(SearchForm):
    #fields
    street_text = forms.CharField(label="Straat", required=False)
    house_number_text = forms.CharField(label="Postcode", required=False)
    city_text = forms.CharField(label="Stad", required=False)
    constructiondate = forms.DateField(required=False)
    sellingprice = forms.ChoiceField(choices=PRIJS, label="Prijs", required=False)

    def search(self):
        sqs = super(PropertiesSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['street_text']:
            sqs = sqs.filter(street_text=self.cleaned_data['street_text'])

        if self.cleaned_data['house_number_text']:
            sqs = sqs.filter(house_number_text=self.cleaned_data['house_number_text'])

        if self.cleaned_data['city_text']:
            sqs = sqs.filter(city_text=self.cleaned_data['city_text'])

        if self.cleaned_data['constructiondate']:
            sqs = sqs.filter(constructiondate=self.cleaned_data['constructiondate'])

        if self.cleaned_data['sellingprice']:
            sqs = sqs.filter(sellingprice=self.cleaned_data['sellingprice'])

        return sqs



class UpdateAccountInformation(forms.ModelForm):

    #TODO: email?
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


