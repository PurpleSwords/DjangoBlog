from django.urls import path

from . import views

urlpatterns = [
	path('login/', views.user_login, name='login'),
	path('logout/', views.uesr_logout, name='logout'),
	path('register/', views.user_register, name='register'),
	path('delete/<int:id>/', views.user_delete, name='delete'),
]
