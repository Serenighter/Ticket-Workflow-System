from django.contrib import admin
from .models import Ticket, Department

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'of_department', 'created_by')
    list_filter = ('status', 'priority', 'of_department')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'closed_at')


admin.site.register(Department)
admin.site.register(Ticket, TicketAdmin)