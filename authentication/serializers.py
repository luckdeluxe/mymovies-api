from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True)
    username = serializers.CharField(
        required=True)
    password = serializers.CharField(
        min_length=8, write_only=True)
    avatar = serializers.ImageField(
        required=False, allow_null=True)
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password', 'avatar')

    def validate_password(self, value):
        return make_password(value)

    def validate_username(self, value):
        value = value.replace(" ", "")  #Since we are we erase the spaces
        try:
            user = get_user_model().objects.get(username=value)
            #If it is the same user by sending the same username, we will let you
            if user == self.instance:
                return value
        except get_user_model().DoesNotExist:
            return value
        raise serializers.ValidationError("Username in use")
    def validate_email(self, value):
        #Is there a user with this email already registered?
        try:
            user = get_user_model().objects.get(email=value)
        except get_user_model().DoesNotExist:
            return value
        #In any other case the validation will fail
        raise serializers.ValidationError("Email in use")

    def update(self, instance, validated_data):
        validated_data.pop('email', None)               #We prevent erasure
        return super().update(instance, validated_data)  #We follow the execution