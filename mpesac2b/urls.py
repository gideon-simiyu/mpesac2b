from django.contrib import admin
from django.urls import path
from user.views import RegisterView, LoginView, HomeView, TransactionView, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('transaction/', TransactionView.as_view(), name='transaction'),
    path('transaction/<account_id>/', TransactionView.as_view(), name='transaction'),
    path('logout/', logout_view, name='logout'),
    path('', HomeView.as_view(), name='home'),
]
