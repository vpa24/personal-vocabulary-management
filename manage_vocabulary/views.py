from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from collections import defaultdict
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import Count

from .models import User, Word, WordEntry
from django.contrib.auth.decorators import login_required

from .authentication.forms import SignupForm, LoginForm
from .VocabularyForm import VocabularyForm
from .VocabularyFormEntry import VocabularyFormEntry
from .forms.SearchForm import SearchForm


def index(request):
    if request.user.is_authenticated:
        context = vocabulary_list_index(request)
        return render(request, 'manage_vocabulary/index_user_is_authenticated.html', context)
    else:
        return render(request, 'manage_vocabulary/index.html')


def login_view(request):
    message = ''
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('index')
        message = 'Invalid username and/or password.'
    return render(request, 'manage_vocabulary/login.html', context={'form': form, 'message': message})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                first_error = errors[0] if errors else ''
                message = first_error
                break
            return render(request, 'manage_vocabulary/register.html', {'form': form, 'message': message})
    else:
        form = SignupForm()

    return render(request, 'manage_vocabulary/register.html', {'form': form})


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
        form_entries = VocabularyFormEntry()
        return render(request, 'manage_vocabulary/add_vocabulary.html', {'form': form, 'form_entries': form_entries})


@login_required()
def search(request):
    form = SearchForm()
    voca_name = ""
    if request.method == 'GET':
        form = SearchForm(request.GET)  # Bind form data to the submitted GET data
        if form.is_valid():
            voca_name = request.GET.get('search')
    return search_vocabulary_list(request, voca_name, form)


def search_vocabulary_list(request, voca_name, form):
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    vocabulary_words = Word.objects.filter(
        owners=user, name__contains=voca_name)
    if len(vocabulary_words) == 1:
        id = vocabulary_words[0].id
        if vocabulary_words[0].name == voca_name:
            return HttpResponseRedirect(reverse('vocabulary_detail', args=(id,)))
    context = {
        'total': len(vocabulary_words),
        'voca_name': voca_name,
        "words": vocabulary_words,
        "searchForm": form
    }
    return render(request, 'manage_vocabulary/search.html', context)


def vocabulary_list_index(request):
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
        'searchForm': SearchForm()
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


@login_required()
def vocab_by_dates(request):
    context = vocabulary_list_monthly(request)
    return render(request, 'manage_vocabulary/vocab_by_dates.html', context)

def vocabulary_list_monthly(request):
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    vocabulary_words = Word.objects.filter(owners=user).order_by('added_date')
    years = vocabulary_words.annotate(year=ExtractYear('added_date')).values('year').distinct().order_by('year')
    months = vocabulary_words.annotate(month=ExtractMonth('added_date')).values('month', 'added_date__month').distinct().order_by('month').annotate(total_words=Count('id'))

    context = {
        'years': years,
        'months': months,
        'vocabulary_words': vocabulary_words,
    }
    return context

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
