from django.contrib import admin
from .models import Host, Meeting

# Register your models here.

class ModifyAdmin(admin.ModelAdmin):
    list_display = ['id','visitor_name','visitor_phone','date','time_in','time_out']
    search_fields = ['id','visitor_name','visitor_phone']


admin.site.register(Host)
admin.site.register(Meeting, ModifyAdmin)
