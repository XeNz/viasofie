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
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from realestate.models import ClientUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=False)

    class Meta:
        model = ClientUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = ClientUser
        fields = ('email', 'password', 'is_active', 'is_admin')

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
    list_display = ('email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
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
    fields = ['property_id','characteristic_id','value','required',]

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

admin.site.register(Property, PropertyAdmin)
admin.site.register(Characteristic, CharacteristicAdmin)
admin.site.register(CurrentStatus, CurrentStatusAdmin)
admin.site.register(FAQ)
admin.site.register(Deal, DealAdmin)
admin.site.register(Status)
admin.site.register(PropertyType, PropertyTypeAdmin)
admin.site.register(Partner, PartnerAdmin)
