#coding:utf8
import threading

from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend


class PublicEmailBackend(EmailBackend):
    
    def __init__(self, host=None, port=None, username=None, password=None,
                 use_tls=None, fail_silently=False, **kwargs):
        
        if hasattr(settings, 'PUBLIC_EMAIL_HOST'):
            host = host or settings.PUBLIC_EMAIL_HOST
        if hasattr(settings, 'PUBLIC_EMAIL_PORT'):
            port = port or settings.PUBLIC_EMAIL_PORT
        if hasattr(settings, 'PUBLIC_EMAIL_HOST_USER'):
            username = username or settings.PUBLIC_EMAIL_HOST_USER
        if hasattr(settings, 'PUBLIC_EMAIL_HOST_PASSWORD'):
            password = password or settings.PUBLIC_EMAIL_HOST_PASSWORD
        if hasattr(settings, 'PUBLIC_EMAIL_USE_TLS'):
            use_tls = use_tls or settings.PUBLIC_EMAIL_USE_TLS
        
        super(PublicEmailBackend, self).__init__(host, port, username, password, use_tls, fail_silently, **kwargs)
