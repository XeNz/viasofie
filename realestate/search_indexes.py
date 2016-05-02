from django.utils import timezone
from haystack import indexes

from .models import Property


class PropertyIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='id')
    title = indexes.CharField(model_attr='title_text')
    street = indexes.CharField(model_attr='street_text')
    postal_code = indexes.CharField(model_attr='postal_code_text')
    city = indexes.CharField(model_attr='city_text')


 
    def get_model(self):
        return Property

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
