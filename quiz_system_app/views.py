from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt

# def home(request):
#      return render (request , "home.html")
def log_in(request):
    if request.method == "POST":
            email = request.POST.get("login_email")
            password = request.POST.get("login_password")
            try :
                user = User.objects.get(email=email)
                if bcrypt.checkpw(password.encode(),user.password.encode()):
                    request.session['user_id'] = user.id
                    return redirect('home')
                else:
                    messages.error(request, "Invalid email or password!")
            except User.DoesNotExist:
                 messages.error(request, "Invalid email or password!")

    return render(request, "log_in_page.html")
def register (request):
    if request.method =="POST":
            errors = User.objects.basic_validator(request.POST)
            if errors:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('register')

            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
            else:
                hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=hashed_pw
                )
                messages.success(request, "Registration successful!")
                return redirect('register')
    return render(request , "register_page.html" )
def logout(request):
    request.session.flush()
    return redirect('log_in')
def home(request):
      user_id = request.session.get('user_id')
      if not user_id:
        return redirect('log_in')  
      user = User.objects.get(id=user_id)
      context = {"user": user}
      return render(request, 'home.html', context)
def about_us (request):
     return render (request , "about_us.html")