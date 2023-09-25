from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class User(AbstractUser):
    time_zone = models.CharField(max_length=50, null=True)

class Word(models.Model):
    name = models.CharField(max_length=100, unique=True)

class WordOwnership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    added_date = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.added_date = timezone.now()
        super(WordOwnership, self).save(*args, **kwargs)
    class Meta:
        unique_together = ('user', 'word')

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
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="word_entries")

    def get_word_type_class(self):
        word_type_classes = {
            'verb': 'badge rounded-pill bg-info',
            'noun': 'badge rounded-pill bg-warning',
            'adjective': 'badge rounded-pill bg-danger',
            'phrasal_verb': 'badge rounded-pill bg-success',
            'adverb': 'badge rounded-pill bg-purple',
        }
        return word_type_classes.get(self.word_type, '')


class Contact(models.Model):
    your_name = models.CharField(max_length=100)
    your_email = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    message = models.TextField()
