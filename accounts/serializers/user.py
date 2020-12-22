from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from accounts.models import Profile


class RegisterUserSerializer(serializers.ModelSerializer):
    contact = PhoneNumberField(required=True)
    address = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ["full_name", "last_name", "username", "email", "password", "contact", "address"]

    @staticmethod
    def validate_full_name(full_name):
        if not full_name:
            raise serializers.ValidationError("This field may not be null.")
        return full_name

    @staticmethod
    def validate_email(email):
        if not email:
            raise serializers.ValidationError("This field may not be null.")
        return email

    @staticmethod
    def validate_password(password):
        if not password:
            raise serializers.ValidationError("This field may not be null.")
        validate_password(password)
        return password

    @staticmethod
    def validate_contact(phone_number):
        try:
            Profile.objects.get(contact=phone_number)
            raise serializers.ValidationError("Contact must be a unique value.")
        except Profile.DoesNotExist:
            return phone_number

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        user_profile = Profile.objects.get(user=user)
        user_profile.full_name = validated_data["full_name"]
        user_profile.contact = validated_data["contact"]
        user_profile.address = validated_data["address"]
        user_profile.save()
        return user


class AddUserSerializer(serializers.ModelSerializer):
    contact = PhoneNumberField(required=True)
    birth_date = serializers.CharField(allow_null=True)
    address = serializers.CharField(required=True)
    full_name = serializers.CharField()

    @staticmethod
    def validate_password(password):
        if not password:
            raise serializers.ValidationError("This field may not be null.")
        validate_password(password)
        return password

    class Meta:
        model = get_user_model()
        fields = ["full_name", "username", "email", "password", "contact", "address", "birth_date"]

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        user_profile = Profile.objects.get(user=user)
        user_profile.full_name = validated_data.get("full_name", "")
        user_profile.contact = validated_data["contact"]
        user_profile.address = validated_data["address"]
        user_profile.birth_date = validated_data["birth_date"]
        user_profile.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    contact = PhoneNumberField(required=True)
    birth_date = serializers.CharField(allow_null=True)
    address = serializers.CharField(required=True)
    full_name = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ["full_name", "username", "email", "contact", "address", "birth_date"]

    def update(self, instance, validated_data):
        profile = instance.profile
        profile.full_name = validated_data.get("full_name", profile.full_name)
        profile.contact = validated_data.get("contact", profile.contact)
        profile.address = validated_data.get("address", profile.address)
        profile.birth_date = validated_data.get("birth_date", profile.birth_date)
        profile.save()
        instance.username = validated_data.get("username", instance.username)
        instance.password = validated_data.get("password", instance.password)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"
        # do not create admins from this api
        read_only_fields = ["is_active", "date_joined", "is_superuser", "is_staff"]
        extra_kwargs = {'password': {'write_only': True}}

    @staticmethod
    def validate_password(password):
        validate_password(password)
        return password

    def create(self, validated_data):
        user = get_user_model().objects.create(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")


class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Profile
        fields = [
            "full_name",
            "bio",
            "contact",
            "birth_date",
            "address",
            "last_updated",
            "image"
        ]


class UserWithProfileSerializer(serializers.ModelSerializer):
    admin = serializers.SerializerMethodField()
    staff = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField()
    profile = ProfileSerializer(read_only=True)

    @staticmethod
    def get_admin(obj):
        return obj.is_superuser

    @staticmethod
    def get_staff(obj):
        return obj.is_staff

    @staticmethod
    def get_last_login(obj):
        if obj.last_login: return '{} days ago'.format((timezone.datetime.now() - obj.last_login).days)
        else: return None

    @staticmethod
    def get_date_joined(obj):
        return '{} days ago'.format((timezone.datetime.now() - obj.date_joined).days)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "admin",
            "staff",
            "date_joined",
            "last_login",
            "profile"
        ]

