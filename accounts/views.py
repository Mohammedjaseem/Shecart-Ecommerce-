from django.shortcuts import render
from .forms import RegistrationForm
from django.contrib import messages, auth
from django.shortcuts import redirect
from .models import Account
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse

#verfication email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


#mail template
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            username = email.split('@')[0]
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            user = Account.objects.create(username=username ,full_name=full_name, email=email, password=password)
            user.phone_number = phone_number
            user.set_password(request.POST['password'])
            user.save()


            #user activation
            current_site = get_current_site(request) #this should be imported 
            mail_subject = 'Activate your Ekka Ecom account.'
            user.save()
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), 
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'Please confirm your email address to complete the registration')
            return redirect('login?command=verification&email='+email)
            
    else:
        form = RegistrationForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            # messages.success(request, 'you are logged in.')
            return redirect('/')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')
        
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'you are logged out.')
    return redirect('login')

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = urlsafe_base64_decode(uidb64)
        user = Account._default_manager.get(pk=uid) 
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and default_token_generator.check_token(user, token):  
        user.is_active = True  
        user.save()  
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login') 

    else:  
        messages.error(request, 'Activation link is invalid!')
        return redirect('register')  


@login_required(login_url='login')
def dashboard(request): 
    return render(request, 'accounts/dashboard.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            
            #reset pasword
            current_site = get_current_site(request) #this should be imported 
            mail_subject = 'Reset your account passowrd.'
            user.save()
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), 
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('login')
        
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgotPassword')

    return render(request, 'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64, token):  
    try:  
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid) 
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and default_token_generator.check_token(user, token):  
        request.session['uid'] = uid
        messages.success(request, 'Please enter your new password.')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Password reset link has been expired!')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid') 
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password has been reset successfully.')
            return redirect('login')

        else:
            messages.error(request, 'Password does not match')
            return redirect('resetPassword')
    else:
        template = 'accounts/resetPassword.html'
        return render(request, template)


def changePassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            user = Account.objects.get(pk=request.user.pk)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password has been reset successfully.')
            return redirect('login')

        else:
            messages.error(request, 'Password does not match')
            return redirect('changePassword')
    else:
        template = 'accounts/changePassword.html'
        return render(request, template)