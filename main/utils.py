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


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))


token_generator = AppTokenGenerator()


def account_activation_email_preparation(request, user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    link = reverse("player_activate", kwargs={
        "uidb64": uidb64,
        "token": token_generator.make_token(user)
    })

    activate_url = "http://" + domain + link

    email_data = {
        "activate_url": activate_url,
        "username": user.username,
        "body": "Activate your account by clicking the link below:\n" + activate_url,
        "body_html": open("templates/emails/account_activation.html").read()
    }

    return email_data


def welcome_email(user):
    email_data = {
        "username": user.username,
        "body": "Welcome to the site! This site is mainly made to keep track our weekly football meetup. Previously, we had to miss a week of play due to miscommunication issue. Hopefully, this website will solve the problem. We hope you enjoy your stay. Cheers!",
        "body_html": open("templates/emails/welcome.html").read()
    }

    return email_data


def send_email_using_ses(to_email, subject, email_data):
    region_name = os.getenv("AWS_REGION_NAME")
    access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    from_email = os.getenv("AWS_FROM_EMAIL")

    CHARSET = "UTF-8"

    client = boto3.client('ses', region_name=region_name,
                          aws_access_key_id=access_key_id,
                          aws_secret_access_key=secret_access_key)

    try:
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
                        'Data': email_data['body_html'].format(body=email_data['body'], username=email_data['username']),
                        'Charset': CHARSET
                    },
                    'Text': {
                        'Data': email_data['body'],
                        'Charset': CHARSET
                    }
                }
            },
            Source=f'Football <{from_email}>',
        )
        return True
    except:
        return False
