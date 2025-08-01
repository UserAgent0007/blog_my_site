from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.



class Post (models.Model):

    class Status (models.TextChoices): # створення власного поля для вибору
                                       # мождиві методи 
                                       # choices - поверне словник з кортежів {('DF', 'Draft'),...}
                                       # values лише службов значення 'DF', 'PB'
                                       # labels зручні підписи поверне
                                       # names - імена змінних -> ['DRAFT', 'PUBLISHED']

        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    
    title = models.CharField (max_length=250)
    slug = models.SlugField (max_length=250) # slugfield - використовує лише цифри, букви, дефіси, нижні підкреслення
    body = models.TextField ()
    publish = models.DateTimeField (default=timezone.now)
    created = models.DateTimeField (auto_now_add=True) # Дата буде збереженна автоматично при створенні об єкта
    updaed = models.DateTimeField (auto_now = True) # дата буде збереженна при модифікації об єкта
    author = models.ForeignKey (settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='blog_posts') # related_name - для того, щоб вказати зворотний зв'язок від User до post

    status = models.CharField (
        max_length=2,
        choices=Status.choices,
        default = Status.DRAFT
    )

    class Meta:

        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title