from django.contrib import admin
from .models import Category

# Register your models here.
#creamos un forma de agilizar el llenado con un autollenado de slug, este tomara el nombre de lo que contenga 
# category_name
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name', )}
    list_display = ('category_name', 'slug')

#agregamos la clase al registro de la administracion para que surga el cambio
admin.site.register(Category, CategoryAdmin)
