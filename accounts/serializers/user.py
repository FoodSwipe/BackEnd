from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from accounts.models import Profile


class RegisterUserSerializer(serializers.ModelSerializer):
    contact = serializers.IntegerField(required=True)
    address = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username", "email", "password", "contact", "address"]

    @staticmethod
    def validate_first_name(first_name):
        if not first_name:
            raise serializers.ValidationError("This field may not be null.")
        return first_name

    @staticmethod
    def validate_last_name(last_name):
        if not last_name:
            raise serializers.ValidationError("This field may not be null.")
        return last_name

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
        phone_number = int(phone_number)
        try:
            Profile.objects.get(contact=phone_number)
            raise serializers.ValidationError("Contact must be a unique value.")
        except Profile.DoesNotExist:
            return phone_number

    def create(self, validated_data):
        user = get_user_model().objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        user_profile = Profile.objects.get(user=user)
        user_profile.contact = validated_data["contact"]
        user_profile.address = validated_data["address"]
        user_profile.save()
        return user


class AddUserSerializer(serializers.ModelSerializer):
    contact = serializers.IntegerField(required=True)
    birth_date = serializers.CharField(allow_null=True)
    address = serializers.CharField(required=True)

    @staticmethod
    def validate_password(password):
        if not password:
            raise serializers.ValidationError("This field may not be null.")
        validate_password(password)
        return password

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username", "email", "password", "contact", "address", "birth_date"]

    def create(self, validated_data):
        user = get_user_model().objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        user_profile = Profile.objects.get(user=user)
        user_profile.contact = validated_data["contact"]
        user_profile.address = validated_data["address"]
        user_profile.birth_date = validated_data["birth_date"]
        user_profile.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    contact = serializers.IntegerField(required=True)
    birth_date = serializers.CharField(allow_null=True)
    address = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username", "email", "contact", "address", "birth_date"]

    def update(self, instance, validated_data):
        profile = instance.profile
        profile.contact = validated_data.get("contact", profile.contact)
        profile.address = validated_data.get("address", profile.address)
        profile.birth_date = validated_data.get("birth_date", profile.birth_date)
        profile.save()
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
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
        fields = ("username", "first_name", "last_name", "email")
