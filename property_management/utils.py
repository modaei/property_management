from rest_framework.serializers import (IntegerField, )
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


class BlankableIntegerField(IntegerField):
    """
    This field is able to receive an empty string for an integer field and turn it into a None number.
    """
    def to_internal_value(self, data):
        if data == '':
            return None
        return super(BlankableIntegerField, self).to_internal_value(data)


def format_file_size(nbytes):
    """
    Converts number of bytes to a human readable format.
    """
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.
        i += 1
    num = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (num, suffixes[i])


def send_mail(context, template):
    """
    Render context data into template and then send the email in text and html formats.
    """
    email_html_message = render_to_string(template + '.html', context)
    email_plaintext_message = render_to_string(template + '.txt', context)
    msg = EmailMultiAlternatives(
        # title:
        context['title'],
        # message:
        email_plaintext_message,
        # from:
        f'noreply@{settings.SITE_DOMAIN}',
        # to:
        [context['to']]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send(fail_silently=False)
