from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'tickets', views.TicketViewSet, basename='ticket')
router.register(r'departments', views.DepartmentViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    # JWT Authentication endpoints
    path('auth/login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    
    path('dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
    
    path('', include(router.urls)),
]