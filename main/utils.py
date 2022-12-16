import os
import boto3

from six import text_type
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import (DjangoUnicodeDecodeError, force_bytes,
                                   force_text)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))


token_generator = AppTokenGenerator()


def account_activation_email_preparation(request, user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    link = reverse("player_activate", kwargs={
        "uidb64": uidb64,
        "token": token_generator.make_token(user)
    })

    if settings.DEBUG:
        activate_url = "http://127.0.0.1:8000" + link
    else:
        activate_url = "https://football.abdullahalrafi.com.bd" + link

    email_data = {
        "activate_url": activate_url,
        "username": user.username,
        "body_html": open("templates/emails/account_activation.html").read()
    }

    return email_data


def welcome_email(user):
    email_data = {
        "username": user.username,
        "body_html": open("templates/emails/welcome.html").read()
    }

    return email_data


def send_email_using_ses(to_email, subject, email_data):
    if "activate_url" not in email_data:
        email_data["activate_url"] = ""

    region_name = os.getenv("AWS_REGION_NAME")
    access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    from_email = os.getenv("AWS_FROM_EMAIL")

    CHARSET = "UTF-8"

    client = boto3.client('ses', region_name=region_name,
                          aws_access_key_id=access_key_id,
                          aws_secret_access_key=secret_access_key)

    # try:
    response = client.send_email(
        Destination={
            'ToAddresses': [
                to_email,
            ],
        },
        Message={
            'Subject': {
                'Data': subject,
                'Charset': CHARSET
            },
            'Body': {
                'Html': {
                    'Data': email_data['body_html'].format(username=email_data['username'], activate_url=email_data['activate_url']),
                    'Charset': CHARSET
                },
                'Text': {
                    'Data': email_data['body_html'],
                    'Charset': CHARSET
                }
            }
        },
        Source=f'Football <{from_email}>',
    )
    return True
    # except:
    #     return False
