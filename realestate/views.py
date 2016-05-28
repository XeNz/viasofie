from django.shortcuts import render,render_to_response, get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from .models import *
from django.template import RequestContext, Context
from django.template.loader import get_template
from .forms import *
from django.contrib import messages
import operator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render_to_response
# from .forms import PropertiesSearchForm,IndexSearchForm
# from haystack.inputs import AutoQuery, Exact, Clean
# from haystack.query import SearchQuerySet
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderPDF
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.contrib.sites.models import Site
from decimal import Decimal
from itertools import islice, chain

def index(request):
    # form = PropertiesSearchForm(request.GET)
    # if request.GET:
    #     query = form.search()
    #     return render_to_response('realestate/index.html', {'query': query, "form": form}, context_instance=RequestContext(request))
    # else:
         #6 most recent properties
    last_six_properties = Property.objects.all().order_by('-pub_date')[:6]
    last_six_properties_in_ascending_order = reversed(last_six_properties)
    #6 featured properties
    featured_six_properties = Property.objects.filter(featured=True).order_by('-pub_date')[:6]
    featured_six_properties_in_ascending_order = reversed(featured_six_properties)
    return render_to_response('realestate/index.html', {"last_six_properties_in_ascending_order": last_six_properties_in_ascending_order, "featured_six_properties_in_ascending_order" : featured_six_properties_in_ascending_order}, context_instance=RequestContext(request))


# class IndexView(generic.ListView):
#     template_name = 'realestate/index.html'
#     context_object_name = 'latest_property_list'

#     def get_queryset(self):
#         result =  Property.objects.filter(featured='True').order_by('-pub_date')[:5]
#         return result
#     def get_propertyPictures(self):
#     	#return PropertyPicture.objects.all()
#         property_ids = list(Property.objects.all().values_list('id', flat=True))
#         result = PropertyPicture.objects.filter(property__in=property_ids)
#         return result

class DetailView(generic.DetailView):
    model = Property
    template_name = 'realestate/detail.html'
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        #context['characteristics'] = Characteristic.objects.all()
        characteristics_property =Characteristics_property.objects.filter(property_id=self.kwargs['pk'])
        context['characteristics_property'] = characteristics_property
        return context


def faq_list(request):
    queryset_list = FAQ.objects.filter(visible_to_public='True')
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(question__icontains=query)#|
                #Q(answer__icontains=query)
                ).distinct()
    paginator = Paginator(queryset_list, 5) # Show 5 faqs per page
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


def search(request):
    form = PropertiesSearchForm
    if request.GET:
        form = PropertiesSearchForm(request.GET)
        query = form.search()
        return render_to_response('realestate/search.html', {'query': query}, context_instance=RequestContext(request))
    else:
        return render_to_response('realestate/search.html', {"form": form}, context_instance=RequestContext(request))


def contact(request):
    #TODO: implement mailto
    #Have to setup STMP server for this to work
    #fix indentation when uncommenting
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name', '')
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')
            from_email = request.POST.get('from_email', '')
            template = get_template('realestate/contact_template.txt')
            context = Context({
                              'name': subject,
                              'from_email': from_email,
                              'subject': subject,
                              'message': message,
                              })
            content = template.render(context)

            email = EmailMessage(
                                 "Nieuw Via Sofie bericht",
                                 content,
                                 "Via Sofie" + ' ',
                                 #TODO info@viasofie.com
                                 ['de.caluwe.bart@gmail.com'],
                                 headers={'Reply-To': from_email}
                                 )
            email.send()
            messages.success(request, 'Bericht met success verstuurd.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
             messages.error(request, 'Er is iets fout gelopen. Probeer het opnieuw.')
    else:
        form = FeedbackForm()

    return render(request, 'realestate/contact.html', {'form': form})

def share(request):
    if request.method == 'POST':
        form = ShareForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name', '')
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')
            from_email = request.POST.get('from_email', '')
            template = get_template('realestate/contact_template.txt')
            context = Context({
                              'name': subject,
                              'from_email': from_email,
                              'subject': subject,
                              'message': message,
                              })
            content = template.render(context)

            email = EmailMessage(
                                 name + "heeft u een nieuw pand doorgestuurd",
                                 content,
                                 "Via Sofie" + ' ',
                                 #TODO info@viasofie.com
                                 ['de.caluwe.bart@gmail.com'],
                                 headers={'Reply-To': from_email}
                                 )
            email.send()
            messages.success(request, 'Bericht met success verstuurd.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
             messages.error(request, 'Er is iets fout gelopen. Probeer het opnieuw.')
    else:
        url = request.META.get('HTTP_REFERER')
        form = FeedbackForm()
        form.message = request.META.get('HTTP_REFERER')

    return render(request, 'realestate/share.html', {'form': form, 'url': url})


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

# this view will run after successfull login
@login_required
def controlpanel(request):
    if not request.user.is_staff:
        deals =Deal.objects.filter(user=request.user)

        if request.method == 'POST':
            selected_deal_id = request.POST.get('selected_deal_id')
            selected_deal = Deal.objects.filter(id=selected_deal_id)
            selected_deal_documents = DealDocument.objects.filter(deal=selected_deal_id,visible_to_user=True)
            selected_deal_statuses = DealStatus.objects.filter(deal=selected_deal_id)
            selected_deal_visitations = Visitation.objects.filter(deal=selected_deal_id)
            context = {
                'deals': deals,
                'selected_deal': selected_deal,
                'selected_deal_documents': selected_deal_documents,
                'selected_deal_statuses': selected_deal_statuses,
                'selected_deal_visitations': selected_deal_visitations,
            }
            return render(request, 'usercontrolpanel/userpanel.html', context)
        else:
            return render(request, 'usercontrolpanel/userpanel.html', {'deals': deals})
    else:
        #TODO: double login prompt error
        messages.error(request, 'Wou je als admin in loggen? Probeer het admin paneel')
        logout(request)
        return render_to_response('usercontrolpanel/login.html', context_instance=RequestContext(request) )

@login_required
def accountinformation(request):
    if not request.user.is_staff:
        user = request.user
        form = UpdateAccountInformation(request.POST or None, initial={'first_name':user.first_name, 'last_name':user.last_name})
        if request.method == 'POST':
            if form.is_valid():
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.save()
                messages.success(request, 'Account informatie aangepast!')
                return HttpResponseRedirect(reverse('realestate:controlpanel'))
        context = {
            "form": form
        }
        return render(request, "usercontrolpanel/accountinformation.html", context)
    else:
        #TODO: double login prompt error
        messages.error(request, 'Wou je als admin in loggen? Probeer het admin paneel')
        logout(request)
        return render_to_response('usercontrolpanel/login.html', context_instance=RequestContext(request) )


def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='usercontrolpanel/password_reset_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('realestate:login'))


def reset(request):
    current_site = Site.objects.get_current()
    current_site_domain= current_site.domain
    return password_reset(request, template_name='usercontrolpanel/password_reset_form.html',
        email_template_name='usercontrolpanel/password_reset_email.html',
        subject_template_name='usercontrolpanel/password_reset_subject.txt',
        post_reset_redirect=reverse('realestate:login'),
        current_site_domain='current_site.domain'
        )


def about(request):
    return render(request, 'realestate/about.html')

def disclaimer(request):
    return render(request, 'realestate/disclaimer.html')

def partners(request):
    img = Partner.objects.all().order_by('-id')
    return render(request, 'realestate/partners.html', {"img": img})

def sell(request):
    data_dict = {'minprice': 1, 'maxprice' : 1}
    form = IndexSearchForm(data=request.POST or None,initial=data_dict)
    # form.fields['province_choices'].queryset = Location.objects.values_list('provincie',flat=True).distinct()
    #form.fields['borough_choices'].queryset = Location.objects.values_list('gemeente',flat=True).distinct().order_by('gemeente')
    # form.fields['propertytype'].queryset = PropertyType.objects.values_list('name',flat=True).distinct()
    #if request.get -> variable bestaat -> get variable -> objects.filter('provincie'=variabele)
    # if request.method == 'GET':
    #     selected_province = request.GET.get('province_choices')
    #     if selected_province:
    #         forms.ModelChoiceField(queryset=Location.objects.none(),)
    if request.method == 'POST':
        # if form.is_valid():
        listing_type_choice = request.POST.get('listing_type_choices')
        #selected_province = request.POST.get('province_choices')
        selected_borough = request.POST.get('borough_choices')
        bedrooms = request.POST.get('bedrooms')
        bathrooms = request.POST.get('bathrooms')
        surfacearea = request.POST.get('surfacearea')
        if not request.POST['minprice'] or not request.POST['maxprice'] or request.POST['maxprice'] == 0 or request.POST['minprice'] == 0 :
             form.add_error('minprice', 'check prices') 
             return render(request, 'realestate/sell.html',{'form': form,})
        else:
            minprice = request.POST.get('minprice') 
            maxprice = request.POST.get('maxprice') 
        propertyType = request.POST.get('propertytype')
        #to fill
        # locationfilter = Location.objects.select_related().filter(Q(provincie__icontains=selected_province) & Q(gemeente__icontains=selected_borough))
        #to search
        property_list = Property.objects.select_related('propertytype_property__propertyType_id__name').filter(Q(listing_type__icontains=listing_type_choice) & Q(bedrooms_text__gte=bedrooms) & Q(bathrooms_text__gte=bathrooms) & Q(surface_area_text__gte=surfacearea) & Q(sellingprice__gte=minprice) & Q(sellingprice__lte=maxprice) & Q(city_text=selected_borough) & Q(propertytype_property__propertyType_id__name=propertyType))
        result_list = property_list
        return render(request, 'realestate/sell.html',{'form': form,'result_list': result_list})
        # location_list = Location.objects.select_related().filter(Q(provincie__icontains=selected_province) & Q(gemeente__icontains=selected_borough))
        # property_type_list = PropertyType.objects.filter(Q(name__icontains=propertyType))


        #result_list = QuerySetChain(property_list, location_list, property_type_list)
        # for ptype in property_type_list:
        #     property_type_property_list = PropertyType_Property.objects.filter(propertyType_id = ptype.id)
        # for ptp in property_type_property_list:
        #     for property in property_list:
        #         if property.id == ptp.property_id:
        #             filtered_property_type_list += property

        # result_list = list(chain(property_list, location_list, property_type_list))
        # return render(request, 'realestate/sell.html',{'form': form,'result_list': result_list})
        # return render(request, 'realestate/sell.html',{'form': form,'result_list': result_list, 'filtered_property_type_list': filtered_property_type_list})
        # else:
        #     messages.error(request, 'KAPUT')
    return render(request, 'realestate/sell.html',{'form': form})

def rent(request):
    return render(request, 'realestate/rent.html')
