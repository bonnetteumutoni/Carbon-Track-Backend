from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import EmissionsViewSet, RegisterUserView, LoginView, RegisterView, FactoryViewSet, MCUViewSet,UserListView, UserDetailView,  EnergyEntryViewSet, ComplianceViewSet
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from rest_framework.routers import DefaultRouter







router = DefaultRouter()
router.register(r'emissions', EmissionsViewSet, basename='emissions')   
router.register(r'factories', FactoryViewSet)
# router.register(r'users', UserDetailView)
router.register(r'mcus', MCUViewSet)
router.register(r'energy_entries', EnergyEntryViewSet)
router.register(r'compliance', ComplianceViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path("register/", RegisterView.as_view(), name="register"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    
    ]


