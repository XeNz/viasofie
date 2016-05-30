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
from django.contrib.auth.models import AbstractUser
from django.conf import settings


def create_qrcode_path(instance, filename):
    return '/'.join(['qrcodes', str(instance.property.id), filename])

class Property(models.Model):
    #TODO: attribute underscore fix
    id = models.AutoField(primary_key=True)
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title_text = models.CharField(max_length=200)
    description_text = models.TextField()
    street_text = models.CharField(max_length=200)
    house_number_text = models.CharField(max_length=200)
    postal_code_text = models.CharField(max_length=200)
    city_text = models.CharField(max_length=200)
    country_text = models.CharField(max_length=200 ,default='België')
    constructiondate = models.DateField()
    # sellingprice = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'))
    sellingprice = models.IntegerField()
    visible_to_public = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')
    surface_area_text = models.IntegerField()
    bathrooms_text = models.IntegerField()
    bedrooms_text = models.IntegerField()
    LISTING_TYPE_CHOICES = (('Kopen', 'Kopen'), ('Huren', 'Huren'))
    listing_type = models.CharField(choices=LISTING_TYPE_CHOICES, max_length=20, default=1)

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
    postcode = models.IntegerField()
    gemeente = models.CharField(max_length=200)
    provincie = models.CharField(max_length=200)

    def __str__(self):
        return '%s %s %s' % (self.gemeente, self.postcode, self.provincie)
    class Meta():
        verbose_name = 'Locatie'
        verbose_name_plural = 'Locaties'

class PropertyLocation(models.Model):
    id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey('Property')
    location_id = models.ForeignKey(Location, related_name='locationkey')

class PropertyType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Client(AbstractUser):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    def __str__(self):
          return "%s's profile" % self.user

class Characteristic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    class Meta():
        verbose_name = 'Property characteristic'
        verbose_name_plural = 'Property characteristics'



class PropertyType_Property(models.Model):
    id = models.AutoField(primary_key=True)
    propertyType_id = models.ForeignKey(PropertyType, related_name='propertytypekey')
    property_id = models.OneToOneField('Property')

class Characteristics_property(models.Model):
    id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey('Property')
    characteristic_id = models.ForeignKey(Characteristic, related_name='characteristickey')
    value = models.CharField(max_length=255)
    required = models.BooleanField(default=False) #required characteristics e.g. bedrooms, bathrooms

    def __str__(self):
        return self.value

def create_property_images_path(instance, filename):
    return '/'.join(['images', str(instance.property.id), filename])

class PropertyPicture(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        #file limit in megabyte
        megabyte_limit = 5.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    property = models.ForeignKey(Property, related_name='propertykey')
    picture = models.ImageField(upload_to=create_property_images_path, blank=True, validators=[validate_image])

class FAQ(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=200)
    answer = models.TextField()
    visible_to_public = models.BooleanField(default=True)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    class Meta():
        verbose_name = 'Frequently Asked Questions'
        verbose_name_plural = 'Frequently Asked Questions'

class Deal(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.OneToOneField(Property, related_name='propertydealkey')
    user = models.ForeignKey(Client, related_name='userdealkey')

    def __str__(self):
        return self.property.title_text

    class Meta():
        verbose_name = 'Deal'
        verbose_name_plural = 'Deals'


class CurrentStatus(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text


class Status(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    visible_to_user = models.BooleanField(default=True)


    def __str__(self):
        return self.title

    class Meta():
        verbose_name = 'Status'
        verbose_name_plural = 'Statussen'


def create_deal_documents_path(instance, filename):
    return '/'.join(['documents', str(instance.deal.id), filename])


class DealStatus(models.Model):
    status = models.ForeignKey(Status, related_name='Dstatuskey')
    deal = models.ForeignKey(Deal, related_name='dealSkey')
    comment = models.CharField(max_length=50)
    current_status = models.ForeignKey(CurrentStatus, related_name='currentstatuskey')
    date = models.DateField()

class DealDocument(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    document = models.FileField(upload_to=create_deal_documents_path)
    deal = models.ForeignKey(Deal, related_name='dealkey')
    visible_to_user = models.BooleanField(default=False)
    #description description_text = models.TextField()

    def __str__(self):
        return self.title

class Visitation(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    deal = models.ForeignKey(Deal, related_name='dealvisitationkey')
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.status

class Partner(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

def create_partner_images_path(instance, filename):
    return '/'.join(['partners', str(instance.partner.id), filename])

class PartnerLogo(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
            #file limit in megabyte
        megabyte_limit = 5.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    partner = models.ForeignKey(Partner, related_name='partnerkey')
    logo = models.ImageField(upload_to=create_partner_images_path, blank=True, validators=[validate_image])
