from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import UserForm
from .forms import UserRoleForm

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


# Create your views here.
@login_required
def index(request):
    return render(request, 'inventories/index.html')#renders the index page

def manageuser(request):
    user = User.objects.all()#retrieves all items from the database
    context = {'users': user}#the items are passed onto the template  
    return render(request,'registration/manageuser.html', context)#render the manage item page items retrieved from the database

def adduser(request):
    form = UserForm()

    if request.method == 'POST':#checks if the method is post
        form = UserForm(request.POST)#the form instance stores the data from the POST
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

@login_required
def updateuserole(request):
    if request.method == 'POST':
        form = UserRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            # Assuming the user is already logged in and you want to change the role of the current user
            user = request.user
            if role == 'admin':
                user.is_superuser = True  # Grant superuser status
                user.is_staff = True  # Typically admin users are also staff
            else:
                user.is_superuser = False
                user.is_staff = False
            user.save()
            return redirect('some_success_url')  # Redirect to a success page
    else:
        form = UserRoleForm()

    return render(request, 'your_template.html', {'form': form})
