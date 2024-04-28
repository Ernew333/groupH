from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm

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

def edit_account_view(request):
    if request.method != 'POST':
        form = UserChangeForm(instance=request.user)
    else:
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:edit_account')  # Redirect to a success page or home page

    context = {'form': form}
    return render(request, 'account_editing/edit_account.html', context)