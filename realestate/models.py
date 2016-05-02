from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from enumchoicefield import ChoiceEnum, EnumChoiceField



class Property(models.Model):
    #TODO: attribute underscore fix
    id = models.AutoField(primary_key=True)
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title_text = models.CharField(max_length=200)
    description_text = models.TextField()
    address_text = models.CharField(max_length=200)
    constructiondate = models.DateField()
    sellingprice = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'))
    visible_to_public = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title_text

    def get_absolute_url(self):
        return "/%i/" % self.id

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    class Meta():
        verbose_name = 'Eigendom'
        verbose_name_plural = 'Eigendommen'

class Characteristic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    class Meta():
        verbose_name = 'Property characteristic'
        verbose_name_plural = 'Property characteristics'

class Characteristics_property(models.Model):
    id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey('Property')
    characteristic_id = models.ForeignKey(Characteristic, related_name='characteristickey')
    value = models.CharField(max_length=255)

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
    user = models.ForeignKey(User, related_name='userdealkey')

    def __str__(self):
        return self.property.title_text

    class Meta():
        verbose_name = 'Deal'
        verbose_name_plural = 'Deals'

class CurrentStatus(ChoiceEnum):
    planned = "Gepland"
    in_progress = "In behandeling"
    done = "In orde"

#status of a deal
#TODO: deal_status model?
class Status(models.Model):
    id = models.AutoField(primary_key=True)
    #title
    text = models.CharField(max_length=50) #description
    #datum
    #visible to user?
    #done? planned/in progress/done?
    current_status = EnumChoiceField(CurrentStatus, default=CurrentStatus.planned)
    deal = models.ForeignKey(Deal, related_name='dealstatuskey')

    def __str__(self):
        return self.text

    class Meta():
        verbose_name = 'Status'
        verbose_name_plural = 'Statussen'


def create_deal_documents_path(instance, filename):
    return '/'.join(['documents', str(instance.deal.id), filename])


class DealDocument(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    document = models.FileField(upload_to=create_deal_documents_path)
    deal = models.ForeignKey(Deal, related_name='dealkey')
    #boolean visible_to_user?
    #description description_text = models.TextField()

    def __str__(self):
        return self.title




