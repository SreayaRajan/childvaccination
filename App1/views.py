from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages 
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProfileRegistrationForm
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    return render(request, 'index.html')




def register(request):
    print("Request method:", request.method)  # Debug print
    if request.method == 'POST':
        form = ProfileRegistrationForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # Debug print
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:
            print("Form errors:", form.errors)  # Debug print
            messages.error(request, 'There was an error in your registration. Please try again.')
    else:
        form = ProfileRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}! You have successfully logged in.')
                return redirect('profile')  # Replace 'profile' with the name of your profile page view
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'profile.html', {'user': request.user})





# @login_required
# def profile_edit_view(request):
#     user = request.user
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Profile updated successfully!')
#             return redirect('profile')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = ProfileForm(instance=user)

#     context = {
#         'user': user,
#         'form': form
#     }
#     return render(request, 'profile.html', context)


@login_required
def profile_edit_view(request):
    user = request.user

    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Update user attributes based on received data
            for field in ['username', 'email', 'phone_number', 'address', 'child_name', 
                          'whatsapp_number', 'gender', 'date_of_birth', 'disability', 
                          'disability_description']:
                if field in data:
                    if field == 'disability':
                        user.disability = data['disability'] == 'yes'
                    else:
                        setattr(user, field, data[field])

            # Save user instance
            user.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({
        'username': user.username,
        'email': user.email,
        'phone_number': user.phone_number,
        'address': user.address,
        'child_name': user.child_name,
        'whatsapp_number': user.whatsapp_number,
        'gender': user.gender,
        'date_of_birth': user.date_of_birth,
        'disability': user.disability,
        'disability_description': user.disability_description,
    })
def bookup(request):
    return render(request, 'bookup.html')
def about(request):
    return render(request, 'about.html')
def history(request):
    return render(request, 'history.html')