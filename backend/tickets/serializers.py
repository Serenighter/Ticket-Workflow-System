from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Ticket, Department, EmployeeProfile
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        
        try:
            profile = user.employeeprofile
            token['department_id'] = profile.department.id if profile.department else None
            token['department_name'] = profile.department.name if profile.department else None
            token['position'] = profile.position
            token['is_department_manager'] = profile.is_department_manager
        except EmployeeProfile.DoesNotExist:
            token['department_id'] = None
            token['department_name'] = None
            token['position'] = None
            token['is_department_manager'] = False
            
        return token


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), 
        write_only=True, 
        required=False,
        allow_null=True
    )
    position = serializers.CharField(max_length=100, required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    is_department_manager = serializers.BooleanField(default=False, required=False)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 
            'password', 'password_confirm', 'department_id', 
            'position', 'phone_number', 'is_department_manager'
        ]
        extra_kwargs = {
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
            'email': {'required': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        department = validated_data.pop('department_id', None)
        position = validated_data.pop('position', '')
        phone_number = validated_data.pop('phone_number', '')
        is_department_manager = validated_data.pop('is_department_manager', False)
        
        user = User.objects.create_user(**validated_data)
        
        EmployeeProfile.objects.create(
            user=user,
            department=department,
            position=position,
            phone_number=phone_number,
            is_department_manager=is_department_manager,
        )
        
        return user


class EmployeeProfileSerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), 
        source='department', 
        required=False,
        allow_null=True
    )

    class Meta:
        model = EmployeeProfile
        fields = ['department', 'department_id', 'position', 'phone_number', 'is_department_manager']


class UserSerializer(serializers.ModelSerializer):
    profile = EmployeeProfileSerializer(source='employeeprofile', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 
                 'is_staff', 'is_superuser', 'profile']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username


class DepartmentSerializer(serializers.ModelSerializer):
    ticket_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = '__all__'

    def get_ticket_count(self, obj):
        return obj.tickets.count()


class TicketSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned = UserSerializer(read_only=True)
    of_department = DepartmentSerializer(read_only=True)
    
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), 
        write_only=True, 
        source='of_department',
        required=False
    )
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='assigned',
        required=False,
        allow_null=True
    )
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by', 'closed_at')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        
        if 'of_department' not in validated_data:
            try:
                user_profile = self.context['request'].user.employeeprofile
                if user_profile.department:
                    validated_data['of_department'] = user_profile.department
            except EmployeeProfile.DoesNotExist:
                pass
                
        return super().create(validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value