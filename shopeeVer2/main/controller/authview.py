from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from main.forms import CreateUserForm, ProfileForm
from django.contrib import messages

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = CreateUserForm()
    
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                request.session['user_id'] = user.id
                messages.success(request, 'Account was create for ' + user.username)
            
                return redirect('login')
    
        context = {'form':form}
        return render(request, 'main/auth/register.html', context)
    
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username = username, password = password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect('/')
            else:
                messages.info(request,' username OR password is incorrect' )
            
        context = {}
        return render(request, 'main/auth/login.html',context)

def logoutUser(request):
    logout(request)
    if 'user_id' in request.session:
        del request.session['user_id']
        messages.success(request, "Logged out Sucessfully")
    return redirect('/login')

def profileUser(request):
    msg=None
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            msg='Data has been saved'
    form = ProfileForm(instance = request.user)
    return render(request, 'main/auth/profile.html',{'form':form, 'msg':msg})

