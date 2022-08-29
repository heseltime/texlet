from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from texapp.models import User

def signup(request):
	if request.method == 'POST':
		form = NewUserForm(request.POST)

		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, 'Thank you, signup successful: you can process your document now.' )
			return redirect('/')

		messages.error(request, 'Unsuccessful signup: Invalid information entered, please check requirements for all fields.')

	form = NewUserForm()

	return render (request=request, template_name='signup.html', context={'signup_form':form})

def signin(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)

		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')

			user = authenticate(username=username, password=password)

			if user is not None:
				login(request, user)
				messages.info(request, f'Thank you, you have logged in as %s' % request.user.username)
				return redirect('/')

			else:
				messages.error(request, 'Invalid username or password.')
		else:
			messages.error(request, 'Invalid username or password.')

	form = AuthenticationForm()

	return render(request=request, template_name='signin.html', context={'signin_form':form})

def signout(request):
	logout(request)
	messages.info(request, 'You have signed out.') 
	return redirect('/')

@login_required
def delete_account(request):    
    try:
        u = User.objects.get(username = request.user.username)
        u.delete()
        messages.success(request, "You have deleted your account and associated metadata")       

    except User.DoesNotExist:
        messages.error(request, "User does not exist in db")    
        return redirect('/manage-profile')

    return redirect('/')

@login_required
def delete_account_check(request):    
    return render(request=request, template_name='delete_account_check.html')