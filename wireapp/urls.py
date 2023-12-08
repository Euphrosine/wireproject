from django.urls import path
from .views import api_view
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    # Other paths for your app...
    path('api/', api_view, name='api_view'),
    path('', views.overall_view, name='overall_page'),
    path('login/', auth_view.LoginView.as_view(template_name='wireapp/login.html'), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name='wireapp/logout.html'), name="logout"),

]
