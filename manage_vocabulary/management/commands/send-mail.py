from typing import Any
from django.core.management.base import BaseCommand
from manage_vocabulary.models import User, Word, WordEntry, WordOwnership
from django.core.mail import send_mail
from django.conf import settings
import random
from datetime import timedelta, date, datetime
from django.utils.html import format_html
from django.core.mail import EmailMessage


class Command(BaseCommand):
    def handle(self, *arg, **kwargs):
        users = User.objects.filter(is_active=True)
        for user in users:
            words_ownership = WordOwnership.objects.filter(
                user_id=user.id).values_list('word_id', flat=True)
            if len(words_ownership) >= 5:
                random_5_words_onwership = random_5_words(words_ownership)
                print(random_5_words_onwership)
                send_summary_voca_mail(user, random_5_words_onwership)
                print("aldready send")

def random_5_words(words_ownership):
    shuffled_words_ownership = list(words_ownership)
    random.shuffle(shuffled_words_ownership)
    return shuffled_words_ownership[:5]


def send_summary_voca_mail(user, words):
    now = datetime.now()
    date = now.strftime("%m/%d/%Y")
    subject = 'Daily Vocabulary Review on ' + date
    message = format_html('Hi {}, <br>', user.first_name)
    body = format_html(
        "<br>It's time for your daily vocabulary review! By using recall method which can help you remember your vocabulary words in the long term memory 🧠.<br/>")
    body += format_html('Here are the 5 vocabulary words for you to review today.<br/><ol>')
    for word_id in words:
        word = Word.objects.filter(pk=word_id).first()
        body += format_html('<li><b>{}</b><br/>', word.name)
        word_entries = WordEntry.objects.filter(word=word, user=user)
        for word_entry in word_entries:

            body += format_html('- {}: {}<br/>',
                                word_entry.word_type, word_entry.definition)
            body += format_html('<b>Example:</b> {}', word_entry.example)
        body += format_html('</li>')
    body += format_html("</ol><br><b>Please adding more vocabulary words to <a href='happydictionary.net'>this link</a> when you've learned any new words 📚 👍. It's a great way to strengthen your memory muscles 💪.</b>")
    recipient = [user.email] 
    email = EmailMessage(
        subject,
        message +
        body,
        'noreply@happydictionary.net',
        recipient,
    )
    email.content_subtype = 'html'
    email.send()
