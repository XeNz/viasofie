from django.db import models
from django.utils import timezone
from decimal import Decimal



class Property(models.Model):
    id = models.AutoField(primary_key=True)
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title_text = models.CharField(max_length=200)
    description_text = models.CharField(max_length=200)
    adress_text = models.CharField(max_length=200)
    constructiondate = models.DateField()
    sellingprice = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'))
    visible_to_public = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    class Meta():
        verbose_name = 'Eigendom'
        verbose_name_plural = 'Eigendommen'

class Characteristics_property(models.Model):
    id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey('Property')
    characteristic_id = models.ForeignKey('Characteristic')
    value = models.CharField(max_length=255)

    def __unicode__(self):
        return str(self.value)

class Characteristic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name
    class Meta():
        verbose_name = 'Property characteristic'
        verbose_name_plural = 'Property characteristics'

#query doen op instance.propertyid.id
def create_property_images_path(instance, filename):
    return '/'.join(['images', str(instance.property.id), filename])

class PropertyPicture(models.Model):
    property = models.ForeignKey(Property, related_name='propertykey')
    picture = models.ImageField(upload_to=create_property_images_path, blank=True)

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
