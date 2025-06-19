from django.shortcuts import render
from rest_framework import viewsets
from .models import Ticket, Department, EmployeeProfile
from .serializers import TicketSerializer, DepartmentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from .serializers import (
    TicketSerializer, DepartmentSerializer, UserSerializer,
    CustomTokenObtainPairSerializer, UserRegistrationSerializer,
    ChangePasswordSerializer, EmployeeProfileSerializer
)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        user = request.user
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        
        if user_serializer.is_valid():
            user_serializer.save()
            
            profile_data = request.data.get('profile', {})
            if profile_data:
                try:
                    profile = user.employeeprofile
                    profile_serializer = EmployeeProfileSerializer(
                        profile, data=profile_data, partial=True
                    )
                    if profile_serializer.is_valid():
                        profile_serializer.save()
                except EmployeeProfile.DoesNotExist:
                    profile_data['user'] = user.id
                    profile_serializer = EmployeeProfileSerializer(data=profile_data)
                    if profile_serializer.is_valid():
                        profile_serializer.save()
            
            return Response(UserSerializer(user).data)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            return Response({'message': 'Password changed successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response({
                    'message': 'User created successfully',
                    'user': UserSerializer(user).data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'error': f'Failed to create user: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        serializer = UserRegistrationSerializer()
        return Response({
            'fields': serializer.fields.keys(),
            'required_fields': ['username', 'email', 'password', 'password_confirm']
        })


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response({
                    'message': 'User created successfully',
                    'user': UserSerializer(user).data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'error': f'Failed to create user: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'])
    def tickets(self, request, pk=None):
        department = self.get_object()
        tickets = department.tickets.all()
        serializer = TicketSerializer(tickets, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        department = self.get_object()
        employees = User.objects.filter(employeeprofile__department=department)
        serializer = UserSerializer(employees, many=True)
        return Response(serializer.data)


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Ticket.objects.all()
        
        if not user.is_staff:
            try:
                user_department = user.employeeprofile.department
                if user_department:
                    queryset = queryset.filter(of_department=user_department)
                else:
                    queryset = queryset.filter(created_by=user)
            except EmployeeProfile.DoesNotExist:
                queryset = queryset.filter(created_by=user)
        
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        priority_filter = self.request.query_params.get('priority')
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
            
        department_filter = self.request.query_params.get('department')
        if department_filter:
            queryset = queryset.filter(of_department_id=department_filter)
            
        assigned_filter = self.request.query_params.get('assigned')
        if assigned_filter:
            if assigned_filter.lower() == 'me':
                queryset = queryset.filter(assigned=user)
            else:
                queryset = queryset.filter(assigned_id=assigned_filter)
        
        return queryset.select_related('created_by', 'assigned', 'of_department')

    def destroy(self, request, *args, **kwargs):

        ticket = self.get_object()
        
        # Check if user has permission
        if not self.can_delete_ticket(request.user, ticket):
            return Response(
                {'error': 'You do not have permission to delete this ticket'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        ticket_title = ticket.title
        ticket_status = ticket.get_status_display()
        ticket.delete()
        return Response(
            {'message': f'Ticket "{ticket_title}" (Status: {ticket_status}) deleted successfully'}, 
            status=status.HTTP_204_NO_CONTENT
        )

    def can_delete_ticket(self, user, ticket):
        if user.is_superuser:
            return True
        
        if user.is_staff:
            return True
        
        try:
            user_profile = user.employeeprofile
            if (user_profile.is_department_manager and 
                user_profile.department == ticket.of_department):
                return True
        except EmployeeProfile.DoesNotExist:
            pass
        
        if ticket.created_by == user:
            return True
        
        return False

    @action(detail=False, methods=['get'])
    def my_tickets(self, request):
        tickets = Ticket.objects.filter(created_by=request.user)
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def assigned_to_me(self, request):
        tickets = Ticket.objects.filter(assigned=request.user)
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'])
    def bulk_delete_closed(self, request):
        # delete closed tickets
        if not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {'error': 'Only staff members can perform bulk delete'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if request.user.is_superuser or request.user.is_staff:
            closed_tickets = Ticket.objects.filter(status='CLOSED')
        else:
            try:
                user_profile = request.user.employeeprofile
                if user_profile.is_department_manager and user_profile.department:
                    closed_tickets = Ticket.objects.filter(
                        status='CLOSED', 
                        of_department=user_profile.department
                    )
                else:
                    return Response(
                        {'error': 'Insufficient permissions'}, 
                        status=status.HTTP_403_FORBIDDEN
                    )
            except EmployeeProfile.DoesNotExist:
                return Response(
                    {'error': 'Employee profile not found'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        
        deleted_count = closed_tickets.count()
        closed_tickets.delete()
        
        return Response(
            {'message': f'{deleted_count} closed tickets deleted successfully'}, 
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        ticket = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            assignee = User.objects.get(id=user_id)
            ticket.assigned = assignee
            ticket.save()
            
            serializer = self.get_serializer(ticket)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        ticket = self.get_object()
        ticket.status = 'CLOSED'
        ticket.closed_at = timezone.now()
        ticket.save()
        
        serializer = self.get_serializer(ticket)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user
    
    if user.is_staff:
        tickets = Ticket.objects.all()
    else:
        try:
            user_department = user.employeeprofile.department
            if user_department:
                tickets = Ticket.objects.filter(of_department=user_department)
            else:
                tickets = Ticket.objects.filter(created_by=user)
        except EmployeeProfile.DoesNotExist:
            tickets = Ticket.objects.filter(created_by=user)
    
    stats = {
        'total_tickets': tickets.count(),
        'open_tickets': tickets.filter(status='OPEN').count(),
        'in_progress_tickets': tickets.filter(status='IN_PROGRESS').count(),
        'closed_tickets': tickets.filter(status='CLOSED').count(),
        'my_tickets': tickets.filter(created_by=user).count(),
        'assigned_to_me': tickets.filter(assigned=user).count(),
        'urgent_tickets': tickets.filter(priority='URGENT').count(),
        'high_priority_tickets': tickets.filter(priority='HIGH').count(),
    }
    
    priority_stats = {}
    for priority, label in Ticket.PRIORITY_CHOICES:
        priority_stats[priority] = tickets.filter(priority=priority).count()
    
    category_stats = {}
    for category, label in Ticket.CATEGORY_CHOICES:
        category_stats[category] = tickets.filter(category=category).count()
    
    stats['priority_distribution'] = priority_stats
    stats['category_distribution'] = category_stats
    
    return Response(stats)

"""
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
"""