from django.shortcuts import render, redirect
from .register_form import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'users/login.html'



def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

@login_required
def landing_view(request):
    return render(request, 'users/landing.html')


