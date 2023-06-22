from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from collections import defaultdict
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Word, WordEntry
from django.contrib.auth.decorators import login_required
from .VocabularyForm import VocabularyForm
from .VocabularyFormEntry import VocabularyFormEntry


def index(request):
    if request.user.is_authenticated:
        context = vocabulary_list(request)
        return render(request, 'manage_vocabulary/index_user_is_authenticated.html', context)
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
            return render(request, "manage_vocabulary/login.html", {
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
        form = VocabularyForm(request.POST)
        if form.is_valid():
            name = request.POST['name'].lower().strip().replace(' ', '-')
            user_id = request.user.id
            user = User.objects.get(pk=user_id)
            vid = existing_vocabulary(user, name)
            if vid != None:
                return render(request, 'manage_vocabulary/add_vocabulary.html', {'form': form, 'message': 'This vocabulary already exists. If you want to view or edit it', 'id': vid})
            elif shared_vocabulary(user, name, request):
                return HttpResponseRedirect(reverse("index"))
            else:
                add_new_vocabulary(user_id, name, request)
                return HttpResponseRedirect(reverse("index"))
    else:
        form = VocabularyForm()
        return render(request, 'manage_vocabulary/add_vocabulary.html', {'form': form})


def vocabulary_list(request):
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    vocabulary_words = Word.objects.filter(owners=user)
    word_dict = defaultdict(list)
    for word in vocabulary_words:
        first_letter = word.name[0].upper()
        if first_letter in word_dict:
            word_dict[first_letter].append(word)
        else:
            word_dict[first_letter] = [word]
    sorted_word_dict = dict(sorted(word_dict.items()))
    letters = sorted_word_dict.keys()
    context = {
        'total': len(vocabulary_words),
        'sored_word_dict': sorted_word_dict.items(),
        'letters': letters,
    }
    return context


@login_required()
def vocabulary_detail(request, vid):
    user = request.user
    word = get_object_or_404(Word, id=vid)

    word_entries = WordEntry.objects.filter(word=word, user=user)
    return render(request, 'manage_vocabulary/vocabulary_detail.html', {
        'word': word,
        'word_entries': word_entries
    })


@login_required()
def edit_vocabulary(request, title, vid):
    if request.method == 'POST':
        form = VocabularyForm(request.POST)
        if form.is_valid():
            name = request.POST['name'].lower().strip().replace(' ', '-')
            update_vocabulary_name(name, title)

            update_vocabulary_entries(request)
            return HttpResponseRedirect(reverse("index"))

    user = request.user
    word = get_object_or_404(Word, pk=vid)
    word_entries = WordEntry.objects.filter(word=word, user=user)
    # Prepare the initial data for the formset
    form_entries = []
    for entry in word_entries:
        initial_data = {
            'example': entry.example,
            'part_of_speech': entry.word_type,
            'definition': entry.definition,
        }
        form_entries.append(VocabularyFormEntry(initial=initial_data))

    return render(request, 'manage_vocabulary/edit_vocabulary.html', {
        'voca_title': word.name.replace('-', ' '),
        'vid': word.id,
        'form': VocabularyForm(initial={'name': word.name.title()}),
        'form_entries': form_entries
    })


def get_owners_by_vocabulary(name):
    words = Word.objects.filter(name=name)
    if words.exists():
        word = words.first()
        return word.owners.all()
    return None


def add_new_owner(user_id, name):
    new_owner = User.objects.get(pk=user_id)
    word = Word.objects.get(name=name)
    word.owners.add(new_owner)


def add_to_word_entry(request, word, user):
    definitions = request.POST.getlist('definition')
    examples = request.POST.getlist('example')
    part_of_speeches = request.POST.getlist('part_of_speech')
    for i in range(len(definitions)):
        definition = definitions[i]
        example = examples[i]
        part_of_speech = part_of_speeches[i]

        word_entry = WordEntry(
            word_type=part_of_speech,
            definition=definition,
            example=example,
            word=word,
            user=user
        )
        word_entry.save()


def existing_vocabulary(user, name):
    # Check if the vocabulary exists for the current user
    existing_vocabulary = user.words.filter(name=name)
    if existing_vocabulary.exists():
        vid = existing_vocabulary.first().id
        return vid
    else:
        return None


def shared_vocabulary(user, name, request):
    # Check if the vocabulary exists with different owners
    shared_vocabulary = Word.objects.filter(name=name).exclude(owners=user)
    if shared_vocabulary.exists():
        shared_word = shared_vocabulary.first()
        shared_word.owners.add(user)
        vid = shared_word.id
        if vid is not None:
            word = Word.objects.get(pk=vid)
            add_to_word_entry(request, word, user)
            return True
    else:
        return False


def add_new_vocabulary(user_id, name, request):
    user = User.objects.get(pk=user_id)
    new_word = Word(name=name)
    new_word.save()
    new_word.owners.set([user])
    add_to_word_entry(request, new_word, user)

def update_vocabulary_entries(request):
    name = request.POST['name'].lower().strip().replace(' ', '-')
    word = get_object_or_404(Word, name=name)
    delete_word_entries(word, request.user)  # Delete old WordEntry instances
    add_to_word_entry(request, word, request.user)

def delete_word_entries(word, user):
    try:
        word_entries = WordEntry.objects.filter(word=word, user=user)
        word_entries.delete()
    except ObjectDoesNotExist:
        pass

def update_vocabulary_name(get_name, title):
    word = get_object_or_404(Word, name=title)
    if title != get_name:
        word.name = get_name
        word.save()
        return
