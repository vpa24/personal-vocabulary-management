from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class User(AbstractUser):
    pass


class Word(models.Model):
    name = models.CharField(max_length=100)
    owners = models.ManyToManyField(User, blank=True, related_name="words")


class WordEntry(models.Model):
    WORD_TYPES = [
        ('verb', 'Verb'),
        ('noun', 'Noun'),
        ('adjective', 'Adjective'),
        ('phrasal_verb', 'Phrasal Verb'),
        ('adverb', 'Adverb'),
    ]
    word_type = models.CharField(max_length=20, choices=WORD_TYPES)
    definition = models.CharField(max_length=300)
    example = models.TextField()
    word = models.ForeignKey(
        Word, on_delete=models.CASCADE, related_name="word_entries")
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="word_entry")

    def get_word_type_class(self):
        word_type_classes = {
            'verb': 'badge rounded-pill bg-info',
            'noun': 'badge rounded-pill bg-warning',
            'adjective': 'badge rounded-pill bg-danger',
            'phrasal_verb': 'badge rounded-pill bg-success',
            'adverb': 'badge rounded-pill bg-purple',
        }
        return word_type_classes.get(self.word_type, '')
