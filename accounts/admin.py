from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

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

#le paso la clase al registro account
# Register your models here.
admin.site.register(Account, AccountAdmin)