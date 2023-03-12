"""witchquiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from .views import login
from .views import home, stage, tick, download, howto

from .apis.api import QuizViewSet
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()


urlpatterns = [
    path('login/', login.LoginView.as_view(), name='login'),
    path('howto/', howto.HowToView.as_view(), name='howto'),
    path('', home.View.as_view(), name='index'),
    path('<int:stage>', stage.View.as_view(), name='stage'),
    path('<int:stage>/<int:tick>', tick.View.as_view(), name='tick'),
    path('api/', include(router.urls)),
    path('api/quiz/', QuizViewSet.as_view()),
    path('download/<int:stage>/', download.download, name='download')
]
