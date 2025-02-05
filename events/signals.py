from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from events.models import Event
from django.conf import settings

@receiver(m2m_changed, sender=Event.participant.through)
def send_event_book_notification(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for user_id in pk_set:
            user = User.objects.get(id=user_id)

            subject = 'Event Booking Confirmation.'
            message = f"Hello, {user.username}\n\n You are successfully booked the event: `{instance.name}`.\n" \
                    f"Date: {instance.date}\nTime: {instance.time}\nLocation: {instance.location}\n\nThank You."
            recipient_list = [user.email]
            
            try:
                send_mail(subject,message,settings.EMAIL_HOST_USER,recipient_list)
            except Exception as e:
                print(f"Failed to send mail to {user.email}: {str(e)}")