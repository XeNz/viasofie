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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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


def faq_list(request):
    queryset_list = FAQ.objects.filter(visible_to_public='True')
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(question__icontains=query)#|
                #Q(answer__icontains=query)
                ).distinct()
    paginator = Paginator(queryset_list, 10) # Show 10 faqs per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)


    context = {
        "object_list": queryset, 
        "page_request_var": page_request_var,
    }
    return render(request, "realestate/faq.html", context)


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