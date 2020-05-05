from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout,login
from django.http import HttpResponse, HttpResponseRedirect
from .models import Note
from .forms import NoteForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        username_form = request.POST.get('username')
        email_form = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password-repeat')

        if password1 == password2 :
            user = User.objects.create_user(username=username_form, email=email_form, password=password1)
            return HttpResponseRedirect('login/')
        else :
            error = 'Passwords are not matching!'
            return render(request, 'home.html', {error})

    else:
        return render(request, 'home.html', {})

def login_view(request):
    if  request.method == 'POST':
        username    = request.POST.get('username')
        password    = request.POST.get('password')
        user        = authenticate(
            username=username,
            password=password
        )
        if user:
            login(request,user)
            return redirect('notes_page')
        else:
            error = " Sorry! Username and Password didn't match, Please try again ! "
            return render(request, 'login.html', {'error': error})

    else:
        return render(request, 'login.html', {})

def logout_view(request):
    if User.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def notes_view(request):
    notes   = Note.objects.filter(user=request.user)
    title   = Note.title
    hour    = Note.hour
    date    = Note.date
    content = {
        'notes':notes,
        'title':title,
        'hour' :hour,
        'date' :date
    }
    return render(request, 'notes.html', content)

def create_view(request):
    form = NoteForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post=form.save(commit=False)
        post.user = request.user
        post.save()
        return redirect('notes_page')

    return render(request,'create.html', {'form':form})

def delete_view(request, id):
    post = get_object_or_404(Note, id=id)
    post.delete()
    return redirect('notes_page')

def display_view(request, id):
    note = get_object_or_404(Note, id=id)
    title = note.title
    if request.user != note.user:
        return redirect('/')
    content = {
        'notes': note,
        'title': title,
    }
    return render(request, 'display.html', content)
