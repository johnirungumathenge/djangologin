from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from Login import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request, 'users/index.html')

def signup(request):
    if request.method == "POST":
        # uname = request.POST.get('username')
        uname = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass']
        cpass = request.POST['cpass']

        if User.objects.filter(username=uname):
            messages.error(request, "username already exists")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, 'Email account already exists!')
            return redirect('home')
        
        if len(uname) > 10:
            messages.error(request, 'username must be less than 10 characters')

        if pass1 != cpass:
            messages.error(request, 'password must match!')

        # if uname.isalnum():
        #     messages.error(request, 'password must contain alpha numeric characters')
        #     return redirect('home')

        myuser = User.objects.create_user(uname, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your account is created successfully. we have sent you a confirmation email. please check your account")

        #welcome email
        subject = "welcome to coding"
        message = "Hello " + fname + ' welcome \n'
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('signin')

    return render(request, 'users/signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass']
        
        user = authenticate(username = username, password=pass1)
        if user is not None:
            # for my own context code
            login(request, user)

            fname = user.username
            return render(request, 'users/index.html', {'fname': fname})
        else:
            messages.error(request, 'Incorrect Username and Password')
            return redirect('home')

    return render(request, 'users/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "You have successfully logged out!")
    return redirect(home)