from django import forms

class FeedbackForm(forms.Form):
    email = forms.EmailField(label="Your Email")
    name = forms.CharField(label="Name")
    message = forms.CharField(label="Body",widget=forms.Textarea)