from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html



#crea los status en el dashboard de las columnas en django
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    #aplica un link dependiendo la columno
    list_display_links = ('email', 'first_name', 'last_name', 'is_active' )
    #Nos indica el dato de los logueos
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

#Para inicializar los filtros
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

#--------------------------------------------UserProfile-----------------------------

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')
    
    def thumbnail(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(obj.profile_picture.url))
        else:
            return "No Image"

    thumbnail.short_description = 'Imagen de Perfil'



#le paso la clase al registro account
# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)