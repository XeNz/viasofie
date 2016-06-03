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
    user = models.ForeignKey(ClientUser, related_name='userdealkey')

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

def create_book_path(instance, filename):
    return '/'.join(['books', str(instance.title), filename])

class Ebook(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    summary = models.CharField(max_length=1024)
    book = models.FileField(upload_to=create_book_path)

    def __str__(self):
        return self.title

class EbookRequest(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    emailaddress = models.EmailField(max_length=255)
    requested_books = models.ManyToManyField(Ebook)

class Subscriber(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()

    def __str__(self):
        return self.email

class Newsletter(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return self.title

