from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')
