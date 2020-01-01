from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse
from accounts.forms import ProfileForm, SignupForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            messages.info(request, f"Successfully created user: {user.username}")
            login(request, user)
            return redirect(reverse('accounts:edit-profile'))
        messages.error(request, 'Invalid input: Please fix the appropriate fields and try again.')

    else:
        form = SignupForm()

    return render(request, 'registration/signup.html', {
        'form': form
    })


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.info(request, 'Profile updated.')
            return redirect(reverse('home'))
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'registration/edit_profile.html', {'form': form})


@login_required
def profile(request):
    profile = request.user.profile
    return render(request, 'registration/view_profile.html', {'profile': profile})