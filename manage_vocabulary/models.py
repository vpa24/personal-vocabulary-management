from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Word(models.Model):
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

class WordEntry(models.Model):
    WORD_TYPES = [
        ('verb', 'Verb'),
        ('noun', 'Noun'),
        ('adjective', 'Adjective'),
        ('phrasal_verb', 'Phrasal Verb'),
    ]
    word_type = models.CharField(max_length=20, choices=WORD_TYPES)
    definition = models.CharField(max_length=300)
    example = models.TextField()
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="word_entries")
    
