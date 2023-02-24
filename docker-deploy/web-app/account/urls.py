from django.urls import path, re_path

from .views import SignUpView

from . import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', views.myprof, name='account-prof'),
    path('driver-register/', views.driver_register, name='driver-register'),
    path('profile/edit', views.edit_profile, name='edit-profile'),
    path('profile/edit/change-password', views.passwd_change, name='passwd-change'),
    path('profile/vehicle-info', views.edit_vehicle_info, name='edit-vehicle-info'),
    path('profile/driver', views.quit_driver, name='quit-driver'),
]