from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tickets.urls')),
]
"""
router = routers.DefaultRouter()
router.register(r'tickets', views.TicketViewSet)
router.register(r'departments', views.DepartmentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
"""