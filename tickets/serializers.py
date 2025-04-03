from rest_framework import serializers
from .models import Ticket, Department
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by', 'closed_at')