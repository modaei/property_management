from django.contrib.auth import get_user_model
from geoip2.errors import AddressNotFoundError
from rest_framework.serializers import ModelSerializer, EmailField, ValidationError, Serializer, CharField, \
    SerializerMethodField
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.gis.geoip2 import GeoIP2
from geography.models import Country, City

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


def get_country_id_from_ip(ip):
    try:
        country_code = GeoIP2().country_code(ip)
        country_id = Country.objects.filter(code=country_code).first().id
    except (AddressNotFoundError, AttributeError):
        country_id = Country.objects.filter(code='US').first().id
    return country_id


def get_city_id_from_ip(ip):
    try:
        city_name = GeoIP2().city(ip)
        city_id = City.objects.filter(name=city_name).filter(country_id=get_country_id_from_ip(ip)).first().id
    except (AddressNotFoundError, AttributeError):
        city_id = None
    return city_id


class UserRetrieveUpdateSerializer(ModelSerializer):
    """
    Serializer for retrieving and updating user account info
    """
    country = SerializerMethodField()
    city = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'email_verified', 'phone_number_verified',
                  'default_country', 'country', 'city']
        read_only_fields = ['id', 'email', 'email_verified', 'phone_number_verified']

    def get_country(self, obj):
        if obj.default_country:
            return obj.default_country.id

        ip = self.get_ip()
        return get_country_id_from_ip(ip)

    def get_city(self, obj):
        if obj.default_city:
            return obj.default_city.id

        ip = self.get_ip()
        return get_city_id_from_ip(ip)

    def get_ip(self):
        x_forwarded_for = self.context.get('request').META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.context.get('request').META.get('REMOTE_ADDR')
        return ip


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
