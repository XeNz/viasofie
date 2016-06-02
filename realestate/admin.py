from django.contrib import admin
from .models import *
from django.contrib.sites.models import Site
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderPDF
from datetime import datetime
from django import forms
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from realestate.models import ClientUser
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.utils.translation import gettext as _
import random
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    username = forms.CharField(label='Username')
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=False)

    widgets = {'username': forms.CharField(required=True),'first_name': forms.CharField(required=True),'last_name': forms.CharField(required=True)}
    class Meta:
        model = ClientUser
        fields = ('first_name','last_name','email','username',)
        # field_classes = {'username': UsernameField}
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        #Make random password of 12 chars if empty
        if len(password1) == 0 and len(password2) == 0:
            password1=''.join([random.choice('1234567890azertyuiopqsdfghjklmwxcvbn') for i in range(12)])
            password2 = password1
        return password2


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])   
        username = self.cleaned_data.get("username")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        if commit:      
            user.save()


        #MAKE THE FUCKING MAIL HERE
        # send_mail('Subject here', 'Here is the password: .'+password,
        #        'from@example.com', ['someone@gmail.com'],
        #        fail_silently=False)
        
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = ClientUser
        fields = ('email', 'password', 'is_active', 'is_admin', 'username','first_name','last_name')
        # field_classes = {'username': UsernameField}
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class ClientUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'username','is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'first_name', 'last_name')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name','password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(ClientUser, ClientUserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

def qrcode(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')

    for obj in queryset.all():
        id = obj.id

    response['Content-Disposition'] = 'attachment; filename="qrcode.pdf"'

    url = Site.objects.get_current().domain
    #url = "https://127.0.0.1:8000"
    p = canvas.Canvas(response)

    qrw = QrCodeWidget("{0}/property/{1}".format(url, id))
    b = qrw.getBounds()

    w = b[2] - b[0]
    h = b[3] - b[1]

    d = Drawing(45,45,transform = [450./w,0,0,450./h,0,0])
    d.add(qrw)

    renderPDF.draw(d, p, 1, 1)

    p.showPage()
    p.save()
    return  response


class VisitationInline(admin.TabularInline):
    model = Visitation
    fields = ['date', 'status', ]

class PropertyTypePropertyInline(admin.TabularInline):
    model = PropertyType_Property
    fields = ['property_id', 'propertyType_id',]

class PropertyPictureInline(admin.TabularInline):
    model = PropertyPicture
    fields = ['picture',]

class Characteristics_propertyInline(admin.TabularInline):
    model = Characteristics_property
    fields = ['property_id','characteristic_id','value',]

class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("id", "name")
    search_fields = ("id", "name")

class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("id", "name")
    search_fields = ("id", "name")

class PropertyAdmin(admin.ModelAdmin):
    list_display = ("title_text", "description_text", "constructiondate", "sellingprice","featured","visible_to_public")
    list_filter = ("sellingprice", "constructiondate","featured")
    search_fields = ("sellingprice",)
    inlines = [PropertyTypePropertyInline, PropertyPictureInline,Characteristics_propertyInline ]
    actions =[qrcode]

class DealDocumentInline(admin.TabularInline):
    model = DealDocument
    fields = ['document', 'title', 'visible_to_user',]

class DealStatusInline(admin.TabularInline):
    model = DealStatus
    fields = ['status', 'deal', 'comment','date', 'current_status',]

class DealAdmin(admin.ModelAdmin):
    inlines = [DealDocumentInline, DealStatusInline, VisitationInline,]

class StatusAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "visible_to_user",)
    list_filter = ("title", "description", "visible_to_user",)
    search_fields = ("title", "description", "visible_to_user",)

class CurrentStatusAdmin(admin.ModelAdmin):
    list_display = ("text",)
    list_filter = ("text",)
    search_fields = ("text",)

class PartnerLogoInline(admin.TabularInline):
    model = PartnerLogo
    fields = ['logo',]


class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    list_filter = ("name", "description")
    search_fields = ("name", "description")
    inlines = [PartnerLogoInline,]

class EbookAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_filter = ("id", "title")
    search_fields = ("id", "title")

class EbookRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "emailaddress")
    list_filter = ("id", "name", "emailaddress")
    search_fields = ("id", "name", "emailaddress")

admin.site.register(Property, PropertyAdmin)
admin.site.register(Characteristic, CharacteristicAdmin)
admin.site.register(CurrentStatus, CurrentStatusAdmin)
admin.site.register(FAQ)
admin.site.register(Deal, DealAdmin)
admin.site.register(Status)
admin.site.register(PropertyType, PropertyTypeAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Ebook, EbookAdmin)
admin.site.register(EbookRequest, EbookRequestAdmin)
