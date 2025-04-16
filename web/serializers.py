from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.apps import apps
from rest_framework.exceptions import AuthenticationFailed


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        student = apps.get_model('web','Student').objects.get(user=self.user)
        # Check the user is inactive
        if not student.flag:
            raise AuthenticationFailed("Your account is inactive and can't be accessed. \
                                    Need help? Contact support")

        # Check the user is deleted
        # if customer.is_deleted:
        #     raise AuthenticationFailed("This account has been deleted.")
        
        return data