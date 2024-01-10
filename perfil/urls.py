from django.urls import path
from . import views

app_name = 'perfil'

urlpatterns = [
    path('', views.CriarView.as_view(), name='criar'),
    path('update/<int:pk>/', views.UpdateView.as_view(), name='update'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
