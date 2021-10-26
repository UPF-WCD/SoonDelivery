"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework import routers
from SoonDelivery import views
from django.conf.urls import url
from knox import views as knox_views

router = routers.DefaultRouter()
router.register('test', views.TestView, 'test')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/signup/', include('rest_auth.registration.urls')),
    
    url("^a/register/$", views.RegistrationAPI.as_view()),
    url("^a/login/$", views.LoginAPI.as_view()),
    url("^auth/user/$", views.UserAPI.as_view()),
    url('a/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),


    path('', views.check_list),
    path('create/',views.create_check),
    path('<int:check_id>',views.check_detail),
    
    url(r"^api/auth", include("knox.urls")),
]
