from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm

# Create your views here.
def loginUser(request):
    page = 'login'
    context = {'page':page}
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
        
        # Check user existence    
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            #Log the user in and create a session in the database and add that in the cookie
            login(request, user) 
            return redirect('profiles')
        else:
            messages.error(request,'Username or password is incorrect')
            
    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    logout(request)
    messages.success(request,'User was logged out!')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid() :
            user = form.save(commit=False)  # For tranformation purpose
            user.username = user.username.lower()
            user.save()
            
            messages.success(request, 'User account was created!')
            
            login(request, user) 
            return redirect('profiles')
        
        else:
            messages.error(request, 'An error has occurred during resgistration!')
    
    context = {'page': page, 'form':form}
    return render(request, 'users/login_register.html', context)

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles' : profiles}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context = { 'profile' : profile, 'topSkills' : topSkills, 'otherSkills' : otherSkills}
    return render(request, 'users/user-profile.html', context=context)