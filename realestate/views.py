from django.shortcuts import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from .models import Property,PropertyPicture,FAQ
from django.template import RequestContext
from .forms import *


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


class Faqview(generic.ListView):
    template_name = 'realestate/faq.html'
    context_object_name = 'all_faqs'
    def get_queryset(self):
        result =  FAQ.objects.filter(visible_to_public='True').order_by('-pub_date')
        return result


# def Contact(request):
#     if request.method == "POST":
#         form = FeedbackForm(request.POST)

#         if(form.is_valid()):
#             print(request.POST['name'])
#             print(request.POST['message'])
#             message = "Dank u voor uw feedback. Wij contacteren u zo snel mogelijk"
#         else:
#             message = "Er is iets mis gegaan. Probeer het later opnieuw."
#         return render_to_response('realestate/contact.html',
#                 {'success': message},
#                 context_instance=RequestContext(request))
#     else:
#         return render_to_response('realestate/contact.html',
#                 {'form':FeedbackForm()},
#                 context_instance=RequestContext(request))




def Contact(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            #still have to give success message to div in template
            return HttpResponseRedirect('realestate/contact.html')
    else:
        form = FeedbackForm()

    return render(request, 'realestate/contact.html', {'form': form})