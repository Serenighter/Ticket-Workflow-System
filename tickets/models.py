from django.db import models
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

class Department(models.Model):
    name = models.CharField("Nazwa działu", max_length=100, unique=True)
    description = models.TextField("Opis", blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    contact_email = models.EmailField("Email kontaktowy", blank=True)
    identification = models.CharField("ID działu", max_length=10, unique=True, default=None)

    class Meta:
        verbose_name = "Dział"
        verbose_name_plural = "Działy"
        ordering = ['name']

    def __str__(self):
        return f"{self.identification} - {self.name}"

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    position = models.CharField("Stanowisko", max_length=100)
    is_department_manager = models.BooleanField(default=False)

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Otwarty'),
        ('IN_PROGRESS', 'W trakcie...'),
        ('CLOSED', 'Zamknięty'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Niski'),
        ('MEDIUM', 'Średni'),
        ('HIGH', 'Wysoki'),
        ('URGENT', 'Najwyższy'),
    ]

    CATEGORY_CHOICES = [
        ('HARDWARE_FAILURE', 'Problem ze sprzętem'),
        ('SOFTWARE_FAILURE', 'Problem z oprogramowaniem'),
        ('DEVICE_NEEDS', 'Zapotrzebowanie na sprzęt'),
    ]

    title = models.CharField("Tytuł", max_length=100)
    description = models.TextField("Opis problemu")
    category = models.CharField("Ketegoria zgłoszenia", max_length=32, choices=CATEGORY_CHOICES, default=None)
    status = models.CharField("Status zgłoszenia", max_length=20, choices=STATUS_CHOICES, default='OPEN')
    priority = models.CharField("Priorytet zgłoszenia", max_length=20, choices=PRIORITY_CHOICES, default='LOW')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Zgłaszający", on_delete=models.PROTECT)
    of_department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='tickets')
    assigned = models.ForeignKey(User, verbose_name="Przypisane do", on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    due = models.DateTimeField("Termin realizacji", null=True, blank=True)
    closed_at = models.DateTimeField("Zgłoszenie zamknięte", null=True, blank=True)

    class Meta:
        verbose_name = "Zgłoszenie"
        verbose_name_plural = "Zgłoszenia"
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title}]"