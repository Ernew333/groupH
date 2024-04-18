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