from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('control_panel/', views.control_panel, name='control_panel'),
    path('preview_data/', views.preview_data, name='preview_data'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('camera_stream/', views.camera_stream, name='camera_stream'),
    path('take_picture/', views.take_picture, name='take_picture'),
    path('system_architecture/', views.system_architecture, name='system_architecture'),
]