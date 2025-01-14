from django.urls import path
from .views import ProfileView, UpdateProfile # type: ignore


urlpatterns = [
    path('<int:pk>/', ProfileView.as_view(), name = 'profile'),
    path('<int:pk>/update/', UpdateProfile.as_view(), name='update-profile'),
]