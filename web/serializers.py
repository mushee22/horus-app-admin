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

class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model =Student
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.user_data = kwargs.pop('user',None)
        return super().__init__(*args, **kwargs)
    
    def update(self, instance, validated_data):
        if self.user_data:
            if CustomUser.objects.filter(
                username=self.user_data.get('username')
            ).exclude(id=instance.user.id).exists():
                raise serializers.ValidationError("Username exists")
            elif CustomUser.objects.filter(
                mobile=self.user_data.get('mobile')
            ).exclude(id=instance.user.id).exists():
                raise serializers.ValidationError("Mobile exists")
            else:
                for attr,value in self.user_data.items():
                    setattr(instance.user,attr,value)
                isinstance.user.save()
        return super().update(instance, validated_data)

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class PurchasedPackagesSerializer(serializers.ModelSerializer):
    course_name = CourseSerializer()
    class Meta:
        model = Purchase
        fields = '__all__'

class PersonalProfileSerilizer(serializers.ModelSerializer):
    purchases = PurchasedPackagesSerializer(source='purchased_student',many=True,read_only=True)
    # purchases = serializers.SerializerMethodField()
    user = CustomUserSerializer()
    class Meta:
        model = Student
        fields = '__all__'

    # def get_purchases(self,obj):
    #     purchase_success = obj.purchased_student.filter(status="success")
    #     return PurchasedPackagesSerializer(purchase_success,many=True).data
