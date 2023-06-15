from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Group(models.Model):
    definition = models.CharField(max_length=300)
    example = models.TextField()

class PartOfSpeech(models.Model):
    WORD_TYPES = [
        ('verb', 'Verb'),
        ('noun', 'Noun'),
        ('adjective', 'Adjective'),
        ('phrasal_verb', 'Phrasal Verb'),
    ]
    word_type = models.CharField(max_length=20, choices=WORD_TYPES)
    groups = models.ManyToManyField(Group, blank=True, related_name="groups")
    
class Word(models.Model):
    name = models.CharField(max_length=100)
    word_types = models.ManyToManyField(PartOfSpeech, blank=True, related_name="word_types")
