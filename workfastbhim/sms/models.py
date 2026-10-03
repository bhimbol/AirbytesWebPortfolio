from django.db import models

class TwilioMessages(models.Model):
    sender_number = models.CharField(max_length=20)
    twilio_number = models.CharField(max_length=20)
    message_body = models.TextField()
    message_sid = models.CharField(max_length=255)
    num_media = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.sender_number} - {self.message_body}"
