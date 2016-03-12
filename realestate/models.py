from django.db import models
from django.utils import timezone
from decimal import Decimal



class Property(models.Model):
    id = models.AutoField(primary_key=True)
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title_text = models.CharField(max_length=200)
    description_text = models.CharField(max_length=200)
    adress_text = models.CharField(max_length=200)
    mailbox = models.CharField(max_length=200,blank=True)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    toilets = models.IntegerField(default=0)
    gardens = models.IntegerField(default=0)
    terraces = models.IntegerField(default=0)
    sellingprice = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'))
    constructiondate = models.DateField()
    visible_to_public = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    PropertyPicture = None

    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.title_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1) 
    class Meta():
        verbose_name = 'Eigendom'
        verbose_name_plural = 'Eigendommen'
#query doen op instance.propertyid.id
def create_property_images_path(instance, filename):
    return '/'.join(['images', str(instance.property.id), filename])
    
class PropertyPicture(models.Model):
    property = models.ForeignKey('Property')
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