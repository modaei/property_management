from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserCreateSerializer, UserRetrieveUpdateSerializer, ChangePasswordSerializer, \
    RequestValidationTokenSerializer, ValidateValidationTokenSerializer, JWTokenPairSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, UpdateAPIView
from .permissions import IsUserInfoOwner
from rest_framework.response import Response
from ..models import ValidationToken
from django.contrib.auth.password_validation import password_changed
from rest_framework import status
import uuid
import random
from django.conf import settings
from smtplib import SMTPException
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


class RegisterAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserRetrieveUpdateAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserRetrieveUpdateSerializer
    permission_classes = [IsAuthenticated, IsUserInfoOwner, ]

    def get_object(self):
        obj = self.request.user
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_destroy(self, instance):
        instance.active = False
        instance.save()


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        user_obj = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data.get("new_password")
            user_obj.set_password(new_password)
            user_obj.save()
            password_changed(new_password, user_obj)
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Validate user contact details by sending a token: Email or phone number
class RequestValidationTokenView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestValidationTokenSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user_obj = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validation_type = serializer.validated_data.get("validation_type")
            ValidationToken.objects.filter(user=user_obj).filter(validation_type=validation_type).delete()
            if validation_type == 'email':
                if user_obj.email_verified:
                    return Response({'non_field_errors': ['Email already verified.']},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    token = uuid.uuid4().hex

                    context = {
                        'title': 'Verify your email address',
                        'full_name': user_obj.full_name,
                        'verify_email_url': f'{settings.VERIFY_EMAIL_URL}{token}',
                        'to': user_obj.email,
                    }
                    try:
                        send_mail(context, 'user_email_verify')
                    except SMTPException:
                        return Response({'non_field_errors': ['error while sending verification email']},
                                        status=status.HTTP_404_NOT_FOUND)

                    ValidationToken.objects.create(
                        user=user_obj,
                        validation_type=validation_type,
                        token=token
                    )
                    response = {
                        'status': 'success',
                        'code': status.HTTP_200_OK,
                        'message': 'verification email sent',
                        'data': []
                    }
                    return Response(response)
            elif validation_type == 'phone':
                if user_obj.phone_number_verified:
                    return Response({'non_field_errors': ['Phone number already verified.']},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    if user_obj.phone_number is None:
                        return Response({'non_field_errors': ['No phone number defined.']},
                                        status=status.HTTP_400_BAD_REQUEST)
                token = random.randint(1000, 9999)
                # TODO: send SMS to the client here
                ValidationToken.objects.create(
                    user=user_obj,
                    validation_type=validation_type,
                    token=token
                )
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'verification SMS sent',
                    'data': []
                }
                return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Check the contact details token. If token is valid email_verified or phone_verified will be true
class ConfirmValidationTokenView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ValidateValidationTokenSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        user_obj = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            token_str = serializer.validated_data.get('token')
            token_obj = ValidationToken.objects.filter(user=user_obj).filter(token=token_str).first()
            if token_obj is None:
                return Response({'token': ['Invalid token.']}, status=status.HTTP_404_NOT_FOUND)
            if token_obj.is_expired:
                return Response({'token': ['Expired token.']}, status=status.HTTP_404_NOT_FOUND)
            if token_obj.validation_type == 'email':
                user_obj.email_verified = True
            elif token_obj.validation_type == 'phone':
                user_obj.phone_number_verified = True
            user_obj.save()
            token_obj.delete()
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)


class JWTokenObtainPairView(TokenObtainPairView):
    serializer_class = JWTokenPairSerializer


@receiver(reset_password_token_created)
def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
    context = {
        'full_name': reset_password_token.user.full_name,
        'reset_password_url': f'{settings.RESET_PASSWORD_URL}{reset_password_token.key}',
        'title': f'Password Reset for {settings.SITE_NAME}',
        'to': reset_password_token.user.email,
        'site_name': settings.SITE_NAME
    }
    try:
        send_mail(context, 'user_reset_password')
    except SMTPException:  # Does not work because rest_reset_password library is used !!!
        return Response({'non_field_errors': ['Error while sending password reset email.']},
                        status=status.HTTP_404_NOT_FOUND)


def send_mail(context, template):
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
