from django.contrib import admin

from chat.models import Message, Chat


class MessageAdmin(admin.ModelAdmin):
    """Сообщения"""
    list_display = ['text', 'get_sender_name', 'date']

    def get_sender_name(self, obj):
        return obj.sender.username

    get_sender_name.short_description = 'Sender username'


admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)
