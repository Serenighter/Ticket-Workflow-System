from django.shortcuts import render
from rest_framework import viewsets
from .models import Ticket, Department
from .serializers import TicketSerializer, DepartmentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.utils import timezone

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    #permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    def perform_update(self, serializer):
        if 'status' in serializer.validated_data and serializer.validated_data['status'] == 'CLOSED':
            serializer.save(closed_at=timezone.now())
        else:
            serializer.save()

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
