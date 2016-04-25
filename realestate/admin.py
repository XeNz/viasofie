from django.contrib import admin

from .models import Property,PropertyPicture,FAQ,Characteristic,Characteristics_property,Deal

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
    list_display = ("title_text", "description_text", "address_text", "constructiondate", "sellingprice")
    list_filter = ("address_text", "sellingprice", "constructiondate")
    search_fields = ("address_text", "sellingprice")
    inlines = [PropertyPictureInline,Characteristics_propertyInline,]

admin.site.register(Property, PropertyAdmin)
admin.site.register(Characteristic, CharacteristicAdmin)
admin.site.register(FAQ)
admin.site.register(Deal)
