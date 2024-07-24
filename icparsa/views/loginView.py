from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from company.models import CompanyEmployee
from icparsa.decorators import unauthenticated_user
from icparsa.forms.registerForm import UserForm


def loger(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                employee = CompanyEmployee.objects.get(email=user.email)
            except CompanyEmployee.DoesNotExist:
                return redirect('syem', pk=user.pk)
            return redirect('home')
        else:
            messages.info(request, 'Wrong Username or Password')

    context = {}
    return render(request, 'icparsa/authentication/login.html', context)


def signe_out(request):
    logout(request)
    return redirect('log')


@unauthenticated_user
def registerPage(request):
    form = UserForm
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('log')

    context = {'regForm': form}
    return render(request, 'icparsa/authentication/register.html', context)


def listSystemUsers(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'icparsa/authentication/systemUsers.html', context)
