from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import send_mail
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
            return JsonResponse({'email_error': 'Sorry email in use, choose another one '})
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
            return JsonResponse({'username_error': 'Sorry username in use, choose another one'})
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        form = SignupForm(request.POST)
        return render(request, 'authentication/register.html', {'form': form, 'include_register_script':  True})

    def post(self, request):
        form = SignupForm(request.POST)
        username = request.POST['username']
        user_email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password1']
        if form.is_valid():
            user = User.objects.create_user(
                username=username, email=user_email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.is_active = False
            user.save()
            current_site = request.build_absolute_uri("/")
            email_body = {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }

            link = reverse('activate', kwargs={
                'uidb64': email_body['uid'], 'token': email_body['token']})

            email_subject = 'Please activate your account!'

            activate_url = current_site+link

            email = EmailMessage(
                email_subject,
                'Hi ' + user.username + ','
                '\n Welcome to Happy Dictionary. \n This website helps you manage your vocabulary effortlessly. By adding your vocabulary words with explanations and examples to boost your English skills. With just five words in your list, my website will send you a daily email featuring five random words. Start building your vocabulary library today 😉!\n Please click on the link below to activate your account \n'+activate_url,
                'noreply@happydictionary.net',
                [user_email],
            )
            email.send(fail_silently=False)
            messages.success(
                request, 'Account successfully created. Please check your email to active your account.')
            return redirect('index')
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


class LoginView(View, LoginForm):
    def get(self, request):
        # form = LoginForm()
        return render(request, 'authentication/login.html', context={'form': LoginForm, 'include_register_script':  True})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('index')
                messages.error(
                    request, 'Account is not active, please check your email')
                return render(request, 'authentication/login.html')
            messages.error(
                request, 'Invalid credentials, try again')
            return render(request, 'authentication/login.html', context={'form': LoginForm, 'include_register_script': True})

        messages.error(
            request, 'Please fill out all fields')
        return render(request, 'authentication/login.html', context={'form': LoginForm, 'include_register_script': True})


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        return redirect('index')
