from django.shortcuts import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from .models import Property,PropertyPicture,FAQ
from django.template import RequestContext
from .forms import *
from django.contrib import messages
import operator
from django.db.models import Q


class IndexView(generic.ListView):
    template_name = 'realestate/index.html'
    context_object_name = 'latest_property_list'

    def get_queryset(self):
        result =  Property.objects.filter(featured='True').order_by('-pub_date')[:5] 
        return result
    def get_propertyPictures(self):
    	#return PropertyPicture.objects.all()
        property_ids = list(Property.objects.all().values_list('id', flat=True))
        result = PropertyPicture.objects.filter(property__in=property_ids)
        return result

    # def get_pictures_and_properties(self):
    #     featuredproperties =  Property.objects.filter(featured='True').order_by('-pub_date')[:5] 
    #     property_ids = featuredproperties.all().values_list('id', flat=True)
    #     filtered_images = PropertyPicture.objects.filter(property__in=property_ids)
    #     result = property_ids
    #     result[filtered_images] = filtered_images
    #     return result;
class DetailView(generic.DetailView):
    model = Property
    template_name = 'realestate/detail.html'


class FaqView(generic.ListView):
    template_name = 'realestate/faq.html'
    context_object_name = 'all_faqs'
    def get_queryset(self):
        result =  FAQ.objects.filter(visible_to_public='True').order_by('-pub_date')
        return result





def contact(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            #still have to give success message to div in template
            messages.success(request, 'Bericht met success verstuurd.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Er is iets fout gelopen. Probeer het opnieuw.')
    else:
        form = FeedbackForm()

    return render(request, 'realestate/contact.html', {'form': form})