from django.contrib import admin
from django.urls import path
from . import views
from userapp.views import *

urlpatterns = [
    path('register/' , RegisterView.as_view(),name='register'),
    path('login/' , LoginView.as_view(),name='login'),
    path('user/' , UserView.as_view(),name='user'),
    path('forgotpassword/',ForgotPasswordAPIView.as_view(), name='ForgotPasswordAPIView'),
    path('changepassword/<int:id>',ChangePassword.as_view(), name='UserChangePasswordView'),
    path('newpassword/<str:email>',newpassword.as_view(), name='newpassword'),
    path ('getbyemail/<str:email>',GetByEmail.as_view(),name='GetByEmail'),
    
    path('getallemails/', views.GetAllUsersEmail.as_view(),name='getallemails'),
    path('gettingallusers/', views.GettingAllUsers.as_view(),name='gettingallusers'),
    path('updateuser/<int:pk>/', views.UpdateUser.as_view(),name='upadateUser'),
    path('deleteuser/<int:pk>/', views.DeleteUser.as_view(),name='deleteUser'),
    path('getbyid/<int:pk>/', views.GetById.as_view(),name='getById'),
]