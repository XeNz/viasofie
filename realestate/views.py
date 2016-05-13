from django.shortcuts import render,render_to_response, get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from .models import *
from django.template import RequestContext
from .forms import *
from django.contrib import messages
import operator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from .forms import PropertiesSearchForm
from haystack.inputs import AutoQuery, Exact, Clean
from haystack.query import SearchQuerySet
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderPDF

def index(request):
    form = PropertiesSearchForm(request.GET)
    if request.GET:
        query = form.search()
        return render_to_response('realestate/index.html', {'query': query, "form": form}, context_instance=RequestContext(request))
    else:
        return render_to_response('realestate/index.html', {"form": form}, context_instance=RequestContext(request))


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

PRIJS = (
         ("0"),
         (50000),
         (100000),
         (200000),
         (300000),
         (400000),
         (500000),
         )


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
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')
            from_email = request.POST.get('from_email', '')
            #if subject and message and from_email:
             #   send_mail(subject, message, from_email, ['xentricator@gmail.com'])
            messages.success(request, 'Bericht met success verstuurd.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
             messages.error(request, 'Er is iets fout gelopen. Probeer het opnieuw.')
    else:
        form = FeedbackForm()

    return render(request, 'realestate/contact.html', {'form': form})

# def qrcode(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="qrcode.pdf"'

#     p = canvas.Canvas(response)

#     qrw = QrCodeWidget('127.0.0.1:8000/property/1')
#     b = qrw.getBounds()

#     w = b[2] - b[0]
#     h = b[3] - b[1]

#     d = Drawing(45,45,transform = [450./w,0,0,450./h,0,0])
#     d.add(qrw)

#     renderPDF.draw(d, p, 1, 1)

#     p.showPage()
#     p.save()
#     return  render(request, response)


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
            selected_deal_documents = DealDocument.objects.filter(deal=selected_deal_id)
            selected_deal_statuses = DealStatus.objects.filter(deal=selected_deal_id)
            planned_status = CurrentStatus.planned
            in_progress_status = CurrentStatus.in_progress
            context = {
                'deals': deals,
                'selected_deal': selected_deal,
                'selected_deal_documents': selected_deal_documents,
                'selected_deal_statuses': selected_deal_statuses,
                'planned_status': planned_status,
                'in_progress_status': in_progress_status
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


def about(request):
    return render(request, 'realestate/about.html')

def disclaimer(request):
    return render(request, 'realestate/disclaimer.html')

