from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):
	list_display = ('email', 'first_name','last_name', 'date_joined', 'last_login', 'is_admin', 'is_active')
	search_fields = ('email','first_name','last_name')
	readonly_fields = ('date_joined', 'last_login')

	ordering = ('email',)
	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()
	add_fieldsets  = ()

admin.site.register(User,MyUserAdmin)
# admin.site.register(User)
