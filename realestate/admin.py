from django.contrib import admin

from .models import Property,PropertyPicture,FAQ,Characteristic,Characteristics_property,Deal,DealDocument,Status

class PropertyPictureInline(admin.TabularInline):
    model = PropertyPicture
    fields = ['picture',]

class Characteristics_propertyInline(admin.TabularInline):
    model = Characteristics_property
    fields = ['property_id','characteristic_id','value',]

class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("id", "name")
    search_fields = ("id", "name")

class PropertyAdmin(admin.ModelAdmin):
    list_display = ("title_text", "description_text", "constructiondate", "sellingprice")
    list_filter = ("sellingprice", "constructiondate")
    search_fields = ("sellingprice",)
    inlines = [PropertyPictureInline,Characteristics_propertyInline,]

class DealDocumentInline(admin.TabularInline):
    model = DealDocument
    fields = ['document', 'title', ]

class StatusInline(admin.TabularInline):
    model = Status
    fields = ['text', 'current_status', ]

class DealAdmin(admin.ModelAdmin):
    inlines = [DealDocumentInline, StatusInline, ]

admin.site.register(Property, PropertyAdmin)
admin.site.register(Characteristic, CharacteristicAdmin)
admin.site.register(FAQ)
admin.site.register(Deal, DealAdmin)
