from django import forms

class FeedbackForm(forms.Form):
    email = forms.EmailField(label="E-mail")
    name = forms.CharField(label="Naam")
    message = forms.CharField(label="Vraag",widget=forms.Textarea)