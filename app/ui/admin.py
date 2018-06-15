from django.contrib import admin
from ui.models import UserProfile
# Register your models here.

#admin.site.register(UserProfile)
admin.site.site_header='UI Administration'

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nick_name', 'email', 'full_name')

    def full_name(self, obj):
        return obj.first_name+" "+obj.last_name
    full_name.short_description = 'User Complete Name'

    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        queryset = queryset.order_by('last_name', 'first_name', 'user')
        return queryset


admin.site.register(UserProfile, UserProfileAdmin)
