from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from app.models import CustomUser
# from django.contrib.auth.decorators import login_required

# Login View
class LoginClassView(View):
    def get(self, request):
        user = request.user
        return render(request, "login.html")
           
    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect("home")
        
        return redirect("login")

 

class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")
    
    def post(self, request):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")  

       
        if role not in ['Gold user', 'Silver user', 'Bronze user', 'Unauthenticated user']:
            messages.error(request, "Please select a valid role")
            return redirect('/register/')

        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already taken")
            return redirect('/register/')

        
        user = CustomUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role
        )
        user.set_password(password) 
        user.save()

        messages.success(request, "Account created successfully")
        return redirect('login')  



class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'home.html')



class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('login')
