
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.shortcuts import render

class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "account/signup.html"

def sign_up(request):
    if request.method == 'GET':
        form = CustomUserCreationForm()
        return render(request, 'registration/signup.html', { 'form': form})  