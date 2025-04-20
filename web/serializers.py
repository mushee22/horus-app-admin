from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.apps import apps
from rest_framework.exceptions import AuthenticationFailed
# model imports
from web.models import *


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

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']


class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class PurchasedPackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'

class PersonalProfileSerilizer(serializers.ModelSerializer):
    purchases = PurchasedPackagesSerializer(source='purchased_student',many=True,read_only=True)
    user = CustomUserSerializer()
    class Meta:
        model = Student
        fields = '__all__'