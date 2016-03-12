from django.contrib import admin

from .models import Property,PropertyPicture,FAQ

class PropertyPictureInline(admin.TabularInline):
    model = PropertyPicture
    fields = ['picture',]

class PropertyAdmin(admin.ModelAdmin):
    list_display = ("title_text", "description_text", "adress_text", "constructiondate", "sellingprice")
    list_filter = ("adress_text", "sellingprice", "constructiondate")
    search_fields = ("adress_text", "sellingprice")
    inlines = [PropertyPictureInline,]

admin.site.register(Property, PropertyAdmin)
admin.site.register(FAQ)