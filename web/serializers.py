from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.apps import apps
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed
# model imports
from web.models import *


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        student = apps.get_model('web','Student').objects.get(user=self.user)
        # Check the user is inactive
        if not student.is_active:
            raise AuthenticationFailed("Your account is inactive and can't be accessed. \
                                    Need help? Contact support")

        # Check the user is deleted
        # if customer.is_deleted:
        #     raise AuthenticationFailed("This account has been deleted.")
        
        return data
    
class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'password']

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists. Try different.")
        return value

    def validate_phone(self, value):
        if CustomUser.objects.filter(phone=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists. Try different.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email','phone']

class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class CustomerUpdateSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model =Student
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.user_data = kwargs.pop('user',None)
        print(self.user_data)
        return super().__init__(*args, **kwargs)
    
    def update(self, instance, validated_data):
        if self.user_data:
            if CustomUser.objects.filter(
                email=self.user_data.get('email')
            ).exclude(id=instance.user.id).exists():
                raise serializers.ValidationError("A user with this email already exists. Try different.")
            elif CustomUser.objects.filter(
                phone=self.user_data.get('phone')
            ).exclude(id=instance.user.id).exists():
                raise serializers.ValidationError("A user with this phone number already exists. Try different.")
            else:
                for attr,value in self.user_data.items():
                    setattr(instance.user,attr,value)
                if self.user_data.get('email'):
                    instance.user.username = self.user_data.get('email')
                instance.user.save()
        return super().update(instance, validated_data)
    
    
class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapterProgress
        fields = '__all__'
    

class CourseSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Course
        fields = '__all__'


class ChapterSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    class Meta:
        model = Chapter
        fields = '__all__'

    def get_progress(self, course):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None

        try:
            student = request.user.student 
        except Student.DoesNotExist:
            return None
        
        has_purchased = Purchase.objects.filter(
            student=student, status="success",is_active=True
        ).exists()

        if not has_purchased:
            return None
        
        
        # progress = get_object_or_404(ChapterProgress,student=)
        return PurchasedPackagesSerializer()

        


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
