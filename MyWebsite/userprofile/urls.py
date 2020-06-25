from django.urls import path

from . import views

urlpatterns = [
	path('login/', views.user_login, name='login'),
	path('logout/', views.uesr_logout, name='logout'),
	path('register/', views.user_register, name='register'),
	path('delete/<int:id>/', views.user_delete, name='delete'),
	# 编辑用户信息
	path('edit/<int:id>/', views.profile_edit, name='edit'),
]
