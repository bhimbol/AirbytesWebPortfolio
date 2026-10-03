from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
from twilio.rest import Client
from django.conf import settings
from .models import TwilioMessages
import logging

logger = logging.getLogger(__name__)
@csrf_exempt
@require_POST

def receive_sms(request):
    twilio_signature = request.headers.get('X-Twilio-Signature')
    if twilio_signature:
        incoming_message = request.POST.get('Body', '')
        sender_number = request.POST.get('From', '')
        twilio_number = request.POST.get('To', '')
        message_sid = request.POST.get('MessageSid', '')
        num_media = int(request.POST.get('NumMedia', 0))
        try:
            sms = TwilioMessages(
                sender_number=sender_number,
                twilio_number=twilio_number,
                message_body=incoming_message,
                message_sid=message_sid,
                num_media=num_media,)
            sms.save()
        except Exception as e:
            logger.error(f"Error processing incoming SMS: {e}")
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


def send_sms(request):
    sms_messages = TwilioMessages.objects.all()
    if request.method == 'POST':
        try:
            twilio_account_sid = settings.TWILIO_ACCOUNT_SID
            twilio_auth_token = settings.TWILIO_AUTH_TOKEN
            twilio_phone_number = settings.TWILIO_PHONE_NUMBER
            recipient_number = request.POST.get('recipient_number')
            message_text = request.POST.get('message_body')
            client = Client(twilio_account_sid, twilio_auth_token)
            message = client.messages.create(
                body=message_text,
                from_=twilio_phone_number,
                to=recipient_number)
        except Exception as e:
            return render(request, 'sms_dashboard.html', {'error_message': str(e)})
    return render(request, 'sms_dashboard.html', {'sms_messages': sms_messages})
