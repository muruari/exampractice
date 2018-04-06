from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def current_user(request):
	return User.objects.get(id = request.session['user_id'])

def registration(request):
	return render(request, 'exam/registration.html')

def register(request):
	check = User.objects.validate(request.POST)
	if request.method != 'POST':
		return redirect('/')
	if check[0] == False:
		for error in check[1]:
			messages.add_message(request, messages.INFO, error, extra_tags="registration")
			return redirect('/')
	if check[0] == True:
		hashed_pw = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt())

		user = User.objects.create(
			name = request.POST.get('name'),
			username = request.POST.get('username'),
			password = hashed_pw
		)

		request.session['user_id'] = user.id
		return redirect('/dashboard')

def login(request):
	if request.method != 'POST':
		return redirect('/')
	user = User.objects.filter(username = request.POST.get('username')).first()

	if user and bcrypt.checkpw(request.POST.get('password').encode(), user.password.encode()):
		request.session['user_id'] = user.id
		return redirect('/dashboard')
	else: 
		messages.add_message(request, messages.INFO, 'Your credentials are invalid! Please try again.', extra_tags="login")
		return redirect('/')
	return redirect('/dashboard')

def logout(request):
		request.session.clear()
		return redirect('/')

def dashboard(request):
	return render(request, 'exam/dashboard.html')