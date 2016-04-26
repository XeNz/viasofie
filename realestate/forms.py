from django import forms
<<<<<<< HEAD
from django.contrib.auth.models import User
=======
from django.contrib.auth.models import  User
>>>>>>> origin/master

class FeedbackForm(forms.Form):
    from_email = forms.EmailField(label="E-mail")
    subject = forms.CharField(label="Onderwerp")
    message = forms.CharField(label="Vraag",widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

<<<<<<< HEAD

=======
>>>>>>> origin/master
class UpdateAccountInformation(forms.ModelForm):

    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    class Meta:
        model = User
<<<<<<< HEAD
        fields = ['first_name', 'last_name']
=======
        fields = ['first_name', 'last_name']
>>>>>>> origin/master
