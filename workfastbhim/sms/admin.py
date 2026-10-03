from django.contrib import admin
from .models import TwilioMessages

@admin.register(TwilioMessages)
class TwilioMessagesAdmin(admin.ModelAdmin):
    list_display = ('sender_number', 'twilio_number', 'message_body', 'message_sid', 'num_media')
    search_fields = ('sender_number', 'twilio_number', 'message_body', 'message_sid')
