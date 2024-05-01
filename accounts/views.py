
#Edwin domale 
# Azim Shahul Hameed
#Ernesto Cosentino
# Nayim Amdouni
# Muhammad Ozair Khan
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .forms import UserRegistrationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import UserForm

def manageuser(request):
    return render(request, 'registration/manageuser.html')

def deleteuser(request):
    return render(request, 'registration/delete.html')

def user_form(request):
    return render(request, 'registration/user_form.html')

def index(request):
    return render(request, 'inventories/index.html')

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

@login_required
def index(request):
    return render(request, 'inventories/index.html')#renders the index page

def manageuser(request):
    user = User.objects.all() #Retrieves all the users from the database
    context = {'users': user} #The users are passed onto the template  
    return render(request,'registration/manageuser.html', context) #Renders the manage user page thats been retrieved from the database

def adduser(request):
    form = UserForm()

    if request.method == 'POST': #Checks if the method is POST
        form = UserForm(request.POST) #The form instance stores the data from the POST
        if form.is_valid():
            form.save()
            return redirect('registration:manageuser')
    context = {'form': form}
    return render(request, 'registration/user_form.html', context)

def updateuser(request,id):
    user = User.objects.get(id=id)
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('registration:manageuser')

    context = {'form': form}
    return render(request, 'registration/user_form.html', context)

def deleteuser(request, id):
    user = User.objects.get(id=id)
    context = {'user': user}
    if request.method == 'POST':
        user.delete()
        return redirect('registration:manageuser')
    return render(request, 'registration/delete.html', {'user': user })