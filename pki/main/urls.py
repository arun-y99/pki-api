from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('CSR/',views.CSR ,name='CSR'),
    path('certificate/',views.certificate ,name='certificate'),
    path('register/',views.register ,name='register'),
    path('verify/',views.verify ,name='verify'),
]