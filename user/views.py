import json

from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import  View

from user.models import Account, Transaction
from user.utils import register_url


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

        accounts = Account.objects.all().order_by('-created_at')
        # Set up pagination
        paginator = Paginator(accounts, 25)  # Show 25 accounts per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {'page_obj': page_obj})


    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        paybill = request.POST['shortcode']
        api_key = request.POST['api_key']
        api_secret = request.POST['api_secret']

        context_data = {}

        try:
            Account.objects.get(paybill=paybill)
            context_data["error"] = "Account already exists"
            return render(request, self.template_name, context_data)

        except Account.DoesNotExist:
            try:
                account = Account.objects.create(
                    username=str(username).upper(),
                    email=email,
                    paybill=paybill,
                    api_key=api_key,
                    api_secret=api_secret
                )

                response = register_url(consumer_key=api_key, consumer_secret=api_secret, account_id=account.uid,
                                        shortcode=paybill)
                print("Register URL response:", response)

                if "error" in response:
                    context_data["error"] = response["error"]
                    return render(request, self.template_name, context_data)

                return redirect('home')

            except Exception as e:
                print("Exception occurred during account creation:", e)
                context_data["error"] = "An error occurred while creating account"
                return render(request, self.template_name, context_data)


def logout_view(request):
    logout(request)
    return redirect('login')


@method_decorator(csrf_exempt, name='dispatch')
class TransactionView(View):
    template_name = 'transaction.html'

    def get(self, request):
        if request.user.is_authenticated:
            transactions = Transaction.objects.all().order_by('-created_at')
            paginator = Paginator(transactions, 25)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, self.template_name, {'page_obj': page_obj})

        return redirect('login')

    def post(self, request, account_id):
        # Parse the JSON data from Safaricom
        data = request.POST if request.POST else request.body

        # Safaricom sends JSON, so decode it if needed
        try:
            transaction_data = json.loads(data) if isinstance(data, bytes) else data
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        # Extract fields from the request data
        try:
            account = Account.objects.get(uid=account_id)
            transaction = Transaction.objects.create(
                account=account,
                transaction_type=transaction_data.get('TransactionType', ''),
                transaction_id=transaction_data.get('TransID', ''),
                transaction_time=parse_datetime(transaction_data.get('TransTime', '')),
                transaction_amount=transaction_data.get('TransAmount', 0.00),
                business_short_code=transaction_data.get('BusinessShortCode', ''),
                bill_ref_number=transaction_data.get('BillRefNumber', ''),
                invoice_number=transaction_data.get('InvoiceNumber', None),
                org_account_balance=transaction_data.get('OrgAccountBalance', 0.00),
                third_party_trans_id=transaction_data.get('ThirdPartyTransID', None),
                msisdn=transaction_data.get('MSISDN', ''),
                first_name=transaction_data.get('FirstName', ''),
                middle_name=transaction_data.get('MiddleName', ''),
                last_name=transaction_data.get('LastName', '')
            )
            transaction.save()
            return JsonResponse({'message': 'Transaction saved successfully'}, status=201)

        except Account.DoesNotExist:
            return JsonResponse({'error': 'Account not found'}, status=404)
        except Exception as e:
            print("Error saving transaction:", e)
            return JsonResponse({'error': 'An error occurred'}, status=500)


def get_transactions(request, account_id):
    account = Account.objects.get(uid=account_id)

    transactions = Transaction.objects.filter(account=account, read=False).order_by('-created_at')

    transactions_data = [
        {
            "transaction_type": transaction.transaction_type,
            "transaction_id": transaction.transaction_id,
            "transaction_time": transaction.transaction_time.strftime('%Y-%m-%d %H:%M:%S'),
            "transaction_amount": str(transaction.transaction_amount),
            "business_short_code": transaction.business_short_code,
            "bill_ref_number": transaction.bill_ref_number,
            "invoice_number": transaction.invoice_number,
            "org_account_balance": str(transaction.org_account_balance) if transaction.org_account_balance else None,
            "third_party_trans_id": transaction.third_party_trans_id,
            "msisdn": transaction.msisdn,
            "first_name": transaction.first_name,
            "middle_name": transaction.middle_name,
            "last_name": transaction.last_name,
        }
        for transaction in transactions
    ]

    # Convert to JSON response
    data = {
        "transactions": transactions_data,
    }

    transactions.update(read=True)

    return JsonResponse(data)
