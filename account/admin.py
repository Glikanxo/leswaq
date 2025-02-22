from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import *
# Register your models here.

class AccountAdmin(UserAdmin):
	list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin','is_staff')
	search_fields = ('email', 'username')
	readonly_fields = ('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()
class MiseANiveauAdmin(admin.ModelAdmin):
    readonly_fields = ['code_confirmation']

admin.site.register(Account,AccountAdmin)

admin.site.register(subscriptions)
admin.site.register(MiseANiveau, MiseANiveauAdmin)
admin.site.register(Rating)
admin.site.register(Enfant)