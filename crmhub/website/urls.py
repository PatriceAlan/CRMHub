from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_user, name='login'),
    # path('', views.logout_user, name='logout'),
]
