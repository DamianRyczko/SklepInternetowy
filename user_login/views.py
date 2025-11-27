from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from .forms import UserRegistrationForm, CustomerForm, LoginForm
from django.contrib.auth import login as auth_login, logout


@transaction.atomic
def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            messages.success(request, f"Account created for {user.username}!")
            return redirect("login")
    else:
        user_form = UserRegistrationForm()
        customer_form = CustomerForm()

    context = {
        "user_form": user_form,
        "customer_form": customer_form
    }
    return render(request, "user_login/register.html", context)

def login(request):
    if request.method == "POST":
        login_form = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth_login(request, user)
            messages.success(request, f"Login successful for {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        login_form = LoginForm()

    context = {
        "login_form": login_form
    }
    return render(request, "user_login/login.html", context)

def logout_view(request):
    # This clears the session data and logs the user out
    logout(request)
    messages.info(request, "You have been logged out.")
    # Redirect them back to the homepage (or login page)
    return redirect("home")