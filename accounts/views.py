# accounts/views.py
from django.views import generic
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserProfileForm
from .models import User


class UserRegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:setup')  # Redirect to home or another page after login

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return response
    


class SetupView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/setup_profile.html'
    success_url = reverse_lazy('index')  # Redirect to home or another page after profile setup

    def get_object(self):
        return self.request.user
