from django.contrib import admin
from .models import State
from .models import Position_source
from .models import Category
from .models import Global_param

from django.contrib.admin.models import LogEntry, DELETION #Added for logging users activity
from django.utils.html import escape   #Added for logging users activity
from django.urls import reverse    #Added for logging users activity
from django.utils.safestring import mark_safe    #Added for logging users activity

# Register your models here.
admin.site.register(State)
admin.site.register(Category)
admin.site.register(Position_source)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag'
        ]

    search_fields = [
        'object_repr',
        'change_message'
        ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag'
        ]

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj = None):
        return False
    
    def has_delete_permission(self, request, obj = None):
        return False
    
    def has_view_permission(self, request, obj = None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link  = excape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href = "%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args = [obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"
            

    
        
        
