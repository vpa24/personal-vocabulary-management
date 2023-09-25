from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from collections import defaultdict
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import Count, Subquery, OuterRef
from django.contrib import messages

from .models import User, Word, WordEntry, WordOwnership
from django.contrib.auth.decorators import login_required

from .VocabularyForm import VocabularyForm
from .VocabularyFormEntry import VocabularyFormEntry
from .forms.SearchForm import SearchForm


def index(request):
    if request.user.is_authenticated:
        context = vocabulary_list_index(request)
        return render(request, 'manage_vocabulary/index_user_is_authenticated.html', context)
    else:
        return render(request, 'manage_vocabulary/index.html')


@login_required()
def add_vocabulary(request):
    form_entries = VocabularyFormEntry()
    if request.method == 'POST':
        form = VocabularyForm(request.POST)
        if form.is_valid():
            name = request.POST['name'].strip()
            word = Word.objects.filter(name=name).first()
            user = request.user
            if word:
                word_id = word.id
                users_exist = User.objects.filter(wordownership__word_id=word_id, wordownership__user_id=user.id).exists()
                if users_exist:
                    vocabulary_detail_url = reverse('vocabulary_detail', args=[word_id])
                    messages.error(
                        request, f'This vocabulary already exists. Click <a href="{vocabulary_detail_url}">here</a> to view your vocabulary.')
                    return render(request, 'manage_vocabulary/add_vocabulary.html', {'form': VocabularyForm(), 'form_entries': form_entries })
                else:
                    word_ownership = WordOwnership(user_id=request.user.id, word_id=word_id)
                    word_ownership.save()
                    add_to_word_entry(request,word, user)
                    return HttpResponseRedirect(reverse("index"))
            else:
                add_new_vocabulary(request, user, name)
                return HttpResponseRedirect(reverse("index"))
    else:
        form = VocabularyForm()
        return render(request, 'manage_vocabulary/add_vocabulary.html', {'form': form, 'form_entries': form_entries})


@login_required()
def search(request):
    form = SearchForm()
    voca_name = ""
    if request.method == 'GET':
        # Bind form data to the submitted GET data
        form = SearchForm(request.GET)
        if form.is_valid():
            voca_name = request.GET.get('search')
    return search_vocabulary_list(request, voca_name, form)


def search_vocabulary_list(request, voca_name, form):
    user = request.user
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
    user = request.user
    words = Word.objects.filter(wordownership__user=user).values_list('id','name')
    word_list = [{'id': item[0], 'name': item[1]} for item in words]
    word_dict = defaultdict(list)
    
    for word in word_list:
        first_letter = word['name'][0].upper()
        if first_letter in word_dict:
            word_dict[first_letter].append(word)
        else:
            word_dict[first_letter] = [word]
    sorted_word_dict = dict(sorted(word_dict.items()))
    letters = sorted_word_dict.keys()
    context = {
        'total': len(words),
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
            name = request.POST['name'].strip()
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
        'voca_title': word.name,
        'vid': word.id,
        'form': VocabularyForm(initial={'name': word.name}),
        'form_entries': form_entries
    })


@login_required()
def vocab_by_dates(request):
    context = vocabulary_list_monthly(request)
    return render(request, 'manage_vocabulary/vocab_by_dates.html', context)


def vocabulary_list_monthly(request):
    user = request.user
    word_ownerships = WordOwnership.objects.filter(user=user).order_by('added_date')
    word_ids = word_ownerships.values_list('word_id', flat=True)
    # Filter the Word objects based on the list of word IDs and annotate with 'added_date'
    vocabulary_words = Word.objects.filter(pk__in=word_ids).annotate(
        added_date=Subquery(
            word_ownerships.filter(word_id=OuterRef('pk')).values('added_date')[:1]
        )
    )
    years = word_ownerships.annotate(year=ExtractYear(
        'added_date')).values('year').distinct().order_by('year')
    months = word_ownerships.annotate(month=ExtractMonth('added_date')).values(
        'month', 'added_date__month').distinct().order_by('-month').annotate(total_words=Count('id'))

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

def add_new_vocabulary(request, user, name):
    new_word = Word(name=name)
    new_word.save()
    word_ownership = WordOwnership(user=user, word=new_word)
    word_ownership.save()
    add_to_word_entry(request, new_word, user)

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

def update_vocabulary_entries(request):
    name = request.POST['name'].strip()
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
