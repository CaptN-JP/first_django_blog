from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("login")

    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid and p_form.is_valid:
            u_form.save()
            p_form.save()
        messages.success(request, "User profile updated")

        return redirect("profile")
        """ due to "Post get redirect pattern" , we are using redirect instead of render.
            If we ever reload a browser after submitting a form, a weird msg comes up 
            'are you sure you wanna reload, because the data will be re-submitted'.
            This is because the browser is trying to signal that u will be running a POST
            request by reloading the page.
                So using redirect actually sends a GET request, thus avoiding this situation"""
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {'u_form': u_form, 'p_form': p_form}
    return render(request, "users/profile.html", context)
