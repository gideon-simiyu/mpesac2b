from lib2to3.fixes.fix_input import context
from sqlite3 import IntegrityError

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import  View

from user.models import Account


class RegisterView(View):
    template_name = 'auth-register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        return render(request, self.template_name)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        username = request.POST['email']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        password = request.POST['password']


        context_data = {
            'username': username,
            'firstname': first_name,
            'lastname': last_name,
            'password': password
        }

        if len(password) < 8:
            context_data["error"] = "Password must be at least 8 characters"
            return render(request, 'auth-register.html', context_data)

        try:
            User.objects.get(username=username)
            context_data["error"] = "User with this email already exists"

            return render(request, self.template_name, context_data)

        except User.DoesNotExist:
            User.objects.create_user(username=username, first_name=str(first_name).upper(), last_name=str(last_name).upper(), password=password)
            return redirect('login')


class LoginView(View):
    template_name = 'auth-login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        context_data = {
            'username': username,
            'password': password
        }

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                login(request, user)
                return redirect('home')

            else:
                context_data["error"] = "Invalid login credentials"
                return render(request, self.template_name, context_data)

        except User.DoesNotExist:
            context_data["error"] = "Invalid login credentials"
            return render(request, self.template_name, context_data)

class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        return render(request, self.template_name)


class AddAccountView(View):
    template_name = 'add-account.html'
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        paybill =request.POST['paybill']
        api_key =request.POST['api_key']
        api_secret =request.POST['api_secret']

        context_data = {

        }

        try:
            Account.objects.get(paybill=paybill)

            context_data["error"] = "Account already exists"
            return render(request, self.template_name, context_data)
        except Account.DoesNotExist:
            try:
                Account.objects.create(
                    username=username,
                    email=email,
                    paybill=paybill,
                    api_key=api_key,
                    api_secret=api_secret
                )

            except:
                context_data["error"] = "An error occurred while creating account"
                return render(request, self.template_name, context_data)

