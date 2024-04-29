from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .forms import UserRegistrationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView

# Create your views here.
def register(request):
    if request.method != 'POST':
        form = UserRegistrationForm()
    else:
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('inventories:index')

    context = {'form': form}
    return render(request, 'registration/register.html', context)

class EditAccountView(LoginRequiredMixin, UpdateView):
    template_name = 'account_editing/edit_account.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('accounts:edit_account')

    def get_object(self, queryset=None):
        return self.request.user
    
    