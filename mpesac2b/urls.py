from django.contrib import admin
from django.urls import path
from user.views import RegisterView, LoginView, HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', HomeView.as_view(), name='home'),
]
