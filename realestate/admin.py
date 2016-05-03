from django.contrib import admin

from .models import Property,PropertyPicture,FAQ,Characteristic,Characteristics_property,Deal,DealDocument,Status,DealStatus

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

class DealStatusInline(admin.TabularInline):
    model = DealStatus
    fields = ['status', 'deal', 'comment','date', ]

class DealAdmin(admin.ModelAdmin):
    inlines = [DealDocumentInline, ]

class StatusAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "visible_to_user",)
    list_filter = ("title", "description", "visible_to_user",)
    search_fields = ("title", "description", "visible_to_user",)

admin.site.register(Property, PropertyAdmin)
admin.site.register(Characteristic, CharacteristicAdmin)
admin.site.register(FAQ)
admin.site.register(Deal, DealAdmin)
