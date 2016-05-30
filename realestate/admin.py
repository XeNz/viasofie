from django.contrib import admin
from .models import *
from django.contrib.sites.models import Site
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderPDF
from datetime import datetime



def qrcode(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')

    for obj in queryset.all():
        id = obj.id

    response['Content-Disposition'] = 'attachment; filename="qrcode.pdf"'

    url = Site.objects.get_current().domain
    #url = "https://127.0.0.1:8000"
    p = canvas.Canvas(response)

    qrw = QrCodeWidget("{0}/property/{1}".format(url, id))
    b = qrw.getBounds()

    w = b[2] - b[0]
    h = b[3] - b[1]

    d = Drawing(45,45,transform = [450./w,0,0,450./h,0,0])
    d.add(qrw)

    renderPDF.draw(d, p, 1, 1)

    p.showPage()
    p.save()
    return  response


class VisitationInline(admin.TabularInline):
    model = Visitation
    fields = ['date', 'status', ]

class PropertyTypePropertyInline(admin.TabularInline):
    model = PropertyType_Property
    fields = ['property_id', 'propertyType_id',]

class PropertyPictureInline(admin.TabularInline):
    model = PropertyPicture
    fields = ['picture',]

class Characteristics_propertyInline(admin.TabularInline):
    model = Characteristics_property
    fields = ['property_id','characteristic_id','value','required',]

class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("id", "name")
    search_fields = ("id", "name")

class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("id", "name")
    search_fields = ("id", "name")

class PropertyAdmin(admin.ModelAdmin):
    list_display = ("title_text", "description_text", "constructiondate", "sellingprice","featured","visible_to_public")
    list_filter = ("sellingprice", "constructiondate","featured")
    search_fields = ("sellingprice",)
    inlines = [PropertyTypePropertyInline, PropertyPictureInline,Characteristics_propertyInline ]
    actions =[qrcode]

class DealDocumentInline(admin.TabularInline):
    model = DealDocument
    fields = ['document', 'title', 'visible_to_user',]

class DealStatusInline(admin.TabularInline):
    model = DealStatus
    fields = ['status', 'deal', 'comment','date', 'current_status',]

class DealAdmin(admin.ModelAdmin):
    inlines = [DealDocumentInline, DealStatusInline, VisitationInline,]

class StatusAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "visible_to_user",)
    list_filter = ("title", "description", "visible_to_user",)
    search_fields = ("title", "description", "visible_to_user",)

class CurrentStatusAdmin(admin.ModelAdmin):
    list_display = ("text",)
    list_filter = ("text",)
    search_fields = ("text",)

class PartnerLogoInline(admin.TabularInline):
    model = PartnerLogo
    fields = ['logo',]


class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    list_filter = ("name", "description")
    search_fields = ("name", "description")
    inlines = [PartnerLogoInline,]

admin.site.register(Property, PropertyAdmin)
admin.site.register(Characteristic, CharacteristicAdmin)
admin.site.register(CurrentStatus, CurrentStatusAdmin)
admin.site.register(FAQ)
admin.site.register(Deal, DealAdmin)
admin.site.register(Status)
admin.site.register(PropertyType, PropertyTypeAdmin)
admin.site.register(Partner, PartnerAdmin)
