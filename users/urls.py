from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('landing/', views.landing_view, name='landing'),
]
