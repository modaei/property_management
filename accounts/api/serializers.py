from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, EmailField, ValidationError, Serializer, CharField
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserCreateSerializer(ModelSerializer):
    """
    This serializer is used for registering new users.
    """
    email = EmailField(label='Email address')  # This makes email field required!
    repeat_password = CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'repeat_password']
        extra_kwargs = {"password": {"write_only": True}, }

    def validate_email(self, value):
        """
        Checks the email address to be unique.
        """
        qs = User.objects.filter(email=value)
        if qs.exists():
            raise ValidationError("User with this email already exists.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_repeat_password(self, value):
        password = self.initial_data.get("password")
        if password != value:
            raise ValidationError("This field may not be different from password.")

    def create(self, validated_data):
        user = User(email=validated_data['email'], )
        user.set_password(validated_data['password'])
        user.save()
        return validated_data


class UserRetrieveUpdateSerializer(ModelSerializer):
    """
    Serializer for retrieving and updating user account info
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'email_verified', 'phone_number_verified']
        read_only_fields = ['id', 'email', 'email_verified', 'phone_number_verified']


class ChangePasswordSerializer(Serializer):
    model = User
    old_password = CharField(required=True)
    new_password = CharField(required=True)
    old_password_valid = False

    def validate_old_password(self, value):
        """
        Check that the inputted old password matches the user's current password.
        """
        user_obj = self.context['request'].user
        if not user_obj.check_password(value):
            raise ValidationError("Wrong password.")
        self.old_password_valid = True
        return value

    def validate_new_password(self, value):
        """
        New password should meet the password criteria!
        """
        user_obj = self.context['request'].user
        if self.old_password_valid:
            validate_password(value, user_obj)
        return value


class RequestValidationTokenSerializer(Serializer):
    """
    Used when requesting token to verify user's email address or phone number.
    """
    validation_type = CharField(required=True)

    def validate_validation_type(self, value):
        if value != 'email' and value != 'phone':
            raise ValidationError('Invalid validation type.')
        return value


class ValidateValidationTokenSerializer(Serializer):
    """
    Used to receive a validation token that has been sent to a user.
    """
    token = CharField(required=True)


class JWTokenPairSerializer(TokenObtainPairSerializer):
    """
    Override default simple_JWT's token generator to add user basic info to
    the token over head.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['full_name'] = user.full_name
        token['email'] = user.email
        token['email_verified'] = user.email_verified

        return token
