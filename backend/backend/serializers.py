from rest_framework import serializers
from .models import LoginDetails, CustomUser


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = LoginDetails
        fields = ["username", "password"]

    def create(self, validated_data):
        """Creates a LoginDetails record and links it to a CustomUser"""
        user = CustomUser.objects.create(username=validated_data["username"])
        login_details = LoginDetails.objects.create(user=user, **validated_data)
        return login_details
