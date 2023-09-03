from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.urls import reverse
from django.contrib import auth
from .forms import SignupForm, LoginForm
from manage_vocabulary.models import User


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use, choose another one '})
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if len(username) < 4:
            return JsonResponse({'username_error': 'username must more than 4 characters'})
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use, choose another one'})
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        form = SignupForm(request.POST)
        return render(request, 'authentication/register.html', {'form': form, 'include_register_script':  True})

    def post(self, request):
        form = SignupForm(request.POST)
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        if form.is_valid():
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_body = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }

            link = reverse('activate', kwargs={
                        'uidb64': email_body['uid'], 'token': email_body['token']})

            email_subject = 'Activate your account'

            activate_url = current_site.domain+link

            email = EmailMessage(
                email_subject,
                'Hi '+ user.username + '\n, Welcome to Happy Dictionary. \n Please the link below to activate your account \n'+activate_url,
                'noreply@happydictionary.com',
                [email],
            )
            email.send(fail_silently=False)
            messages.success(request, 'Account successfully created')
            return render(request, 'authentication/register.html', {'form': form, 'include_register_script':  True})
        else:        
            context = {
                'form': form,
                'fieldValues': request.POST,
                'include_register_script':  True
            }

            for field, errors in form.errors.items():
                first_error = errors[0] if errors else ''
                messages.error(
                    request, first_error)
                break
        return render(request, 'authentication/register.html', context)
                    

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'authentication/login.html', context={'form': form, 'include_register_script':  True})

    def post(self, request):
        form = LoginForm()
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('index')
                messages.error(
                    request, 'Account is not active, please check your email')
                return render(request, 'authentication/login.html')
            messages.error(
                request, 'Invalid credentials, try again')
            return render(request, 'authentication/login.html', context={'form': form, 'include_register_script':  True})

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'authentication/login.html', context={'form': form, 'include_register_script':  True})


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        return redirect('index')
