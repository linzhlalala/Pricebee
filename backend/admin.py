from django.contrib import admin
from .models import item,ImportFile
from pbsearch.importcsv import import_data_csv
#from import_export.admin import ImportExportModelAdmin

class itemAdmin(admin.ModelAdmin):
    list_display = ('category_level_2',
        'item_title','item_original_price','item_unit_price',
        'item_discount_price','item_discount_text','item_discount_save','item_source')
    list_display_links = ('item_title',)
    search_fields = ('category_level_2','item_title')
    actions =  ['delete_everything']   

    def delete_everything(self, request, queryset):
        item.objects.all().delete()    

admin.site.register(item, itemAdmin)


class ImportFileAdmin(admin.ModelAdmin):
    list_display=('file','file_name','update_time')

    def save_model(self, request, obj, form, change):
        import_data_csv(request,obj)

        obj.file.delete(False)
        obj.save()

admin.site.register(ImportFile, ImportFileAdmin)

    