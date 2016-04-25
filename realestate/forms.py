from django import forms
from haystack.forms import SearchForm

class FeedbackForm(forms.Form):
    from_email = forms.EmailField(label="E-mail")
    subject = forms.CharField(label="Onderwerp")
    message = forms.CharField(label="Vraag",widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class PropertiesSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()
