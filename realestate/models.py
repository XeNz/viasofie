import io
import os
from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from os.path import join
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.conf import settings
from django.utils.translation import ugettext_lazy as _



class ClientUserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password = None):
        """
        Creates and saves a User with the given username, password, email, created_a
        birth and password.
        """
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password):
        user = self.create_user(username, email, password,first_name,last_name,)
        user.is_admin = True
        user.save(using=self._db)
        return user

class ClientUser(AbstractBaseUser):
    # user = models.ForeignKey(UserL, related_name="clientuserkey")
    username = models.CharField(max_length=100,unique=True,db_index = True,)
    email = models.EmailField(max_length=255,unique=True,)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]
    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)
    objects = ClientUserManager()
    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

def create_qrcode_path(instance, filename):
    return '/'.join(['qrcodes', str(instance.property.id), filename])

class Property(models.Model):
    #TODO: attribute underscore fix
    id = models.AutoField(primary_key=True)
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title_text = models.CharField(max_length=200,verbose_name = _('Property|title_text'))
    description_text = models.TextField(verbose_name = _('Property|description_text'))
    street_text = models.CharField(max_length=200,verbose_name = _('Property|street_text'))
    house_number_text = models.CharField(max_length=200,verbose_name = _('Property|house_number_text'))
    postal_code_text = models.CharField(max_length=200,verbose_name = _('Property|postal_code_text'))
    city_text = models.CharField(max_length=200,verbose_name = _('Property|city_text'))
    country_text = models.CharField(max_length=200 ,default='België',verbose_name = _('Property|country_text'))
    constructiondate = models.DateField(verbose_name = _('Property|constructiondate'))
    # sellingprice = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'))
    sellingprice = models.IntegerField(verbose_name = _('Property|sellingprice'))
    visible_to_public = models.BooleanField(default=True,verbose_name = _('Property|visible_to_public'))
    featured = models.BooleanField(default=False , verbose_name = _('Property|featured'))
    pub_date = models.DateTimeField(verbose_name = _('Property|datepublished'))
    surface_area_text = models.IntegerField(verbose_name = _('Property|surface_area_text'))
    bathrooms_text = models.IntegerField(verbose_name = _('Property|bathrooms_text'))
    bedrooms_text = models.IntegerField(verbose_name = _('Property|bedrooms_text'))
    LISTING_TYPE_CHOICES = (('Kopen', 'Kopen'), ('Huren', 'Huren'))
    listing_type = models.CharField(choices=LISTING_TYPE_CHOICES, max_length=20, default=1, verbose_name = _('Property|listing_type'))

    def get_absolute_url(self):
        return reverse('realestate.views.details', args=[str(self.id)])
    def __str__(self):
        return self.title_text

    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days=1))

    class Meta():
        verbose_name = 'Eigendom'
        verbose_name_plural = 'Eigendommen'

class Location(models.Model):
    id = models.AutoField(primary_key=True)
    postcode = models.IntegerField(verbose_name = _('Location|postcode'))
    gemeente = models.CharField(max_length=200, verbose_name = _('Location|gemeente'))
    provincie = models.CharField(max_length=200 , verbose_name = _('Location|provincie'))

    def __str__(self):
        return '%s %s %s' % (self.gemeente, self.postcode, self.provincie)
    class Meta():
        verbose_name = _('Locatie')
        verbose_name_plural = _('Locaties')

class PropertyLocation(models.Model):
    id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey('Property')
    location_id = models.ForeignKey(Location, related_name='locationkey')

class PropertyType(models.Model):
    id = models.AutoField(primary_key=True, verbose_name = _('PropertyType|id'))
    name = models.CharField(max_length=255 , verbose_name = _('PropertyType|name'))

    def __str__(self):
        return self.name
    class Meta():
        verbose_name = _('Property Type')
        verbose_name_plural = _('Property Types')

class Characteristic(models.Model):
    id = models.AutoField(primary_key=True, verbose_name = _('Characteristic|id'))
    name = models.CharField(max_length=255, verbose_name = _('Characteristic|name'))

    def __str__(self):
        return self.name
    class Meta():
        verbose_name = _('Property characteristic')
        verbose_name_plural = _('Property characteristics')



class PropertyType_Property(models.Model):
    id = models.AutoField(primary_key=True , verbose_name = _('PropertyType_Property|id'))
    propertyType_id = models.ForeignKey(PropertyType, related_name='propertytypekey', verbose_name = _('PropertyType_Property|propertyType_id'))
    property_id = models.OneToOneField('Property', verbose_name = _('PropertyType_Property|property_id'))
    class Meta():
        verbose_name = _('Property Type characteristic')
        verbose_name_plural = _('Property Type characteristics')

class Characteristics_property(models.Model):
    id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey('Property', verbose_name = _('Characteristics_property|property_id'))
    characteristic_id = models.ForeignKey(Characteristic, related_name='characteristickey', verbose_name = _('Characteristics_property|characteristic_id'))
    value = models.CharField(max_length=255, verbose_name = _('Characteristics_property|value'))

    def __str__(self):
        return self.value
    class Meta():
        verbose_name = _('Property characteristic')
        verbose_name_plural = _('Property characteristics')
def create_property_images_path(instance, filename):
    return '/'.join(['images', str(instance.property.id), filename])

class PropertyPicture(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        #file limit in megabyte
        megabyte_limit = 5.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    property = models.ForeignKey(Property, related_name='propertykey', verbose_name = _('PropertyPicture|property') )
    picture = models.ImageField(upload_to=create_property_images_path, blank=True, validators=[validate_image], verbose_name = _('Characteristics_property|picture'))

    class Meta():
        verbose_name = _('Property Picture')
        verbose_name_plural = _('Property Pictures')
class FAQ(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=200,verbose_name = _('FAQ|question'))
    answer = models.TextField(verbose_name = _('FAQ|answer'))
    visible_to_public = models.BooleanField(default=True,verbose_name = _('FAQ|visible_to_public'))
    pub_date = models.DateTimeField(verbose_name = _('FAQ|pub_date'))

    def __str__(self):
        return self.question

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    class Meta():
        verbose_name = _('Frequently Asked Questions')
        verbose_name_plural = _('Frequently Asked Questions')

class Deal(models.Model):
    id = models.AutoField(primary_key=True, verbose_name = _('Deal|id'))
    property = models.OneToOneField(Property, related_name='propertydealkey',verbose_name = _('Deal|property'))
    user = models.ForeignKey(ClientUser, related_name='userdealkey',verbose_name = _('FAQ|user'))

    def __str__(self):
        return self.property.title_text

    class Meta():
        verbose_name = _('Deal')
        verbose_name_plural = _('Deals')


class CurrentStatus(models.Model):
    id = models.AutoField(primary_key=True ,verbose_name = _('CurrentStatus|id'))
    text = models.CharField(max_length=100 ,verbose_name = _('CurrentStatus|text'))

    def __str__(self):
        return self.text


class Status(models.Model):
    id = models.AutoField(primary_key=True ,verbose_name = _('Status|id'))
    title = models.CharField(max_length=50 ,verbose_name = _('Status|title'))
    description = models.CharField(max_length=500 ,verbose_name = _('Status|description'))
    visible_to_user = models.BooleanField(default=True ,verbose_name = _('Status|visible_to_user'))


    def __str__(self):
        return self.title

    class Meta():
        verbose_name = _('Status')
        verbose_name_plural = _('Statussen')


def create_deal_documents_path(instance, filename):
    return '/'.join(['documents', str(instance.deal.id), filename])


class DealStatus(models.Model):
    status = models.ForeignKey(Status, related_name='Dstatuskey',verbose_name = _('DealStatus|status'))
    deal = models.ForeignKey(Deal, related_name='dealSkey',verbose_name = _('DealStatus|deal'))
    comment = models.CharField(max_length=50,verbose_name = _('DealStatus|comment'))
    current_status = models.ForeignKey(CurrentStatus, related_name='currentstatuskey',verbose_name = _('DealStatus|current_status'))
    date = models.DateField(verbose_name = _('DealStatus|date'))

    class Meta():
        verbose_name = _('Status')
        verbose_name_plural = _('Statussen')

class DealDocument(models.Model):
    id = models.AutoField(primary_key=True, verbose_name = _('DealDocument|id'))
    title = models.CharField(max_length=50, verbose_name = _('DealDocument|title'))
    document = models.FileField(upload_to=create_deal_documents_path, verbose_name = _('DealDocument|document'))
    deal = models.ForeignKey(Deal, related_name='dealkey', verbose_name = _('DealDocument|deal'))
    visible_to_user = models.BooleanField(default=False, verbose_name = _('DealDocument|visible_to_user'))
    #description description_text = models.TextField()

    def __str__(self):
        return self.title
    class Meta():
        verbose_name = _('Deal Document')
        verbose_name_plural = _('Deal Documents')
class Visitation(models.Model):
    id = models.AutoField(primary_key=True, verbose_name = _('Visitation|id'))
    date = models.DateField(verbose_name = _('Visitation|date'))
    deal = models.ForeignKey(Deal, related_name='dealvisitationkey', verbose_name = _('Visitation|deal'))
    status = models.CharField(max_length=100, verbose_name = _('Visitation|status'))

    def __str__(self):
        return self.status
    class Meta():
        verbose_name = _('Visitation')
        verbose_name_plural = _('Visitations')

class Partner(models.Model):
    name = models.CharField(max_length=50, verbose_name = _('Partner|name'))
    description = models.CharField(max_length=200, verbose_name = _('Partner|description'))
    url = models.CharField(max_length=200, verbose_name = _('Partner|url'))

def create_partner_images_path(instance, filename):
    return '/'.join(['partners', str(instance.partner.id), filename])

class PartnerLogo(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
            #file limit in megabyte
        megabyte_limit = 5.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    partner = models.ForeignKey(Partner, related_name='partnerkey', verbose_name = _('PartnerLogo|partner'))
    logo = models.ImageField(upload_to=create_partner_images_path, blank=True, validators=[validate_image], verbose_name = _('PartnerLogo|logo'))

def create_book_path(instance, filename):
    return '/'.join(['books', str(instance.title), filename])

class Ebook(models.Model):
    id = models.AutoField(primary_key=True ,verbose_name = _('Ebook|id'))
    title = models.CharField(max_length=50 ,verbose_name = _('Ebook|title'))
    summary = models.CharField(max_length=1024 ,verbose_name = _('Ebook|summary'))
    book = models.FileField(upload_to=create_book_path ,verbose_name = _('Ebook|book'))

    def __str__(self):
        return self.title

class EbookRequest(models.Model):
    id = models.AutoField(primary_key=True, verbose_name = _('EbookRequest|id'))
    name = models.CharField(max_length=200, verbose_name = _('EbookRequest|name'))
    emailaddress = models.EmailField(max_length=255, verbose_name = _('EbookRequest|emailaddress'))
    requested_books = models.ManyToManyField(Ebook, verbose_name = _('EbookRequest|requested_books'))

    class Meta():
        verbose_name = _('Ebook request')
        verbose_name_plural = _('Ebook requests')

