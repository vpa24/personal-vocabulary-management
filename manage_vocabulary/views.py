from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404

from .models import User, Word, WordEntry
from django.contrib.auth.decorators import login_required
from .addVocabularyForm import addVocabularyForm

def index(request):
    if request.user.is_authenticated:
        word_entries = WordEntry.objects.all()
        return render(request,'manage_vocabulary/index_user_is_authenticated.html', {'word_entries': word_entries})
    else:
        return render(request, 'manage_vocabulary/index.html')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "manage_vocaubary/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "manage_vocabulary/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "manage_vocabulary/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "manage_vocabulary/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "manage_vocabulary/register.html")

@login_required()    
def add_vocabulary(request):
    if request.method == 'POST':
        form = addVocabularyForm(request.POST)
        if form.is_valid():
            name = request.POST['name'].lower().strip()
            new_word = Word(name=name)
            new_word.save()

            part_of_speech =request.POST['part_of_speech']
            definition = request.POST['definition']
            example = request.POST['example']
            new_word_entry = WordEntry(word_type= part_of_speech, definition=definition, example=example, word=new_word)
            new_word_entry.save()
            return render(request, 'manage_vocabulary/add_vocabulary.html', {'form': form})
    else:
        form = addVocabularyForm()
        return render(request, 'manage_vocabulary/add_vocabulary.html', {'form': form})
    
def vocabularyList():
    entries = WordEntry.objects.all()
    return entries;

@login_required()
def vocabulary_detail(request, vid):
    word = Word.objects.get(pk=vid)
    word_entries = WordEntry.objects.filter(word=word)
    return render(request, 'manage_vocabulary/vocabulary_detail.html' ,{
        'word': word,
        'word_entries': word_entries
    })