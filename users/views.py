from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.

def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request,
                  'users/user/profile.html',
                  {'user': user})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Create context dictionary to store form data and error flags
        context = {
            'username': username,
            'email': email,
            'username_error': False,
            'email_error': False
        }

        # Check if username already exists (case-insensitive)
        if User.objects.filter(username__iexact=username).exists():
            messages.add_message(request, messages.ERROR,
                                 f"The username '{username}' is already taken. Please choose a different username.")
            context['username_error'] = True
            return render(request, 'users/user/register.html', context)

        # Check if email already exists (case-insensitive)
        if User.objects.filter(email__iexact=email).exists():
            messages.add_message(request, messages.ERROR,
                                 f"The email '{email}' is already registered. Please use a different email address.")
            context['email_error'] = True
            return render(request, 'users/user/register.html', context)

        try:
            # Create new user if validation passes
            user = User.objects.create_user(username, email, password)
            request.session['username'] = user.username
            request.session['role'] = 'user'  # Set default role
            messages.add_message(request, messages.SUCCESS,
                                 f'User created successfully with the username: {username}')
            return redirect('users:profile', username=user.username)

        except Exception as e:
            # Handle unexpected errors
            print(e)
            messages.add_message(request, messages.ERROR,
                                 'An unexpected error occurred. Please try again.')

        return render(request, 'users/user/register.html', context)

    # If not POST request, display empty registration form
    return render(request, 'users/user/register.html')


def login_user(request):
    username = request.POST.get("username")
    pw = request.POST.get("pw")

    user = authenticate(username=username, password=pw)
    if user is not None:
        request.session['username'] = user.username
        request.session['role'] = user.detail.role
        messages.add_message(request, messages.SUCCESS, 'You have logged in successfully!')
    else:
        messages.add_message(request, messages.ERROR, 'Invalid username or password')
    return redirect('page:homeview')


def logout_user(request):
    del request.session['username']
    del request.session['role']
    return redirect('page:homeview')
