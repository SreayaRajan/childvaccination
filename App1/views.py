from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages 
from django.shortcuts import render, redirect
from .forms import ProfileRegistrationForm
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
from django.views import View
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpRequest
from django.conf import settings
import razorpay
import pkg_resources

# from django.contrib.auth.views import PasswordResetView
# from django.urls import reverse_lazy 

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
                return redirect('bookup')  # Replace 'profile' with the name of your profile page view
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required
def profile_view(request:HttpRequest):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile.html')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'profile.html', {'user': request.user})
def forgetpassword(request):
     return render(request, 'forgetpassword.html')
    # if request.method == 'POST':
    #     email = request.POST.get('email')
    #     if User.objects.filter(email=email).exists():
    #         form = PasswordResetForm(request.POST)
    #         if form.is_valid():
    #             form.save(
    #                 request=request,
    #                 use_https=request.is_secure(),
    #                 email_template_name='registration/password_reset_email.html',
    #                 subject_template_name='registration/password_reset_subject.txt',
    #             )
    #         return render(request, 'forgetpassword.html', {'message': 'Password reset email has been sent.'})
    #     else:
    #         return render(request, 'forgetpassword.html', {'error': 'No user with this email address.'})
    






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


class BookingCreateView(View):
    def get(self, request):
        return render(request, 'bookup.html', {'razorpay_key_id': settings.RAZORPAY_KEY_ID})

    def post(self, request):
        vaccinations = request.POST.get('vaccination')
        appointment_date = request.POST.get('date')

        # Check if user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to book a vaccination.")
            return redirect('login')

        # Check if the required fields are filled
        if not vaccinations or not appointment_date:
            messages.error(request, "Please fill in all required fields.")
            return redirect('book_vaccination')

        # Get the user's profile
        profile = request.user

        # Create a new booking entry
        token_number = random.randint(1000, 9999)  # Generate a random token number
        booking = Booking.objects.create(
            patient=profile,
            vaccinations=vaccinations,
            appointment_date=appointment_date,
            token_number=token_number,
            appointment_fee=700.00  # Adjust as needed
        )

        # Create a Razorpay client instance
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Create a Razorpay order
        payment = client.order.create({
            'amount': 700,  # Amount in paise
            'currency': 'INR',
            'payment_capture': '1'  # Auto capture
        })

        booking.razorpay_order_id = payment['id']
        booking.save()

        # Redirect to a success page or send a success message
        messages.success(request, "Your booking has been created successfully!")
        return redirect('success')
def bookup(request):
    return render(request, 'bookup.html')

def success(request):
    booking = Booking.objects.filter(patient=request.user).latest('id')
    return render(request, 'success.html', {'booking': booking})

def about(request):
     return render(request, 'about.html')
def history(request):
    return render(request, 'history.html')
def admin_login(request):
    return render(request, 'adminside/admin_login.html')


