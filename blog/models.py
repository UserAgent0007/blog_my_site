from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

# Create your models here.
class PublishManager (models.Manager): # Можна ще змінювати поведінку функцій create, get_or_create, bulk_create
                                       # Можна змінювати ще сам об єкт QuerySet, тобто створити новий і перепризначити
                                       

    def get_queryset(self):
        return super().get_queryset().filter (status=Post.Status.PUBLISHED)
    


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
    slug = models.SlugField (max_length=250, unique_for_date='publish') # slugfield - використовує лише цифри, букви, дефіси, нижні підкреслення
                                                                        # unique_for_date - об єднує запис slug з publish і перевіряє 
                                                                        # чи є ще такі самі пари, якщо є, то викликається помилка валідації
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

    objects = models.Manager() # для того, щоб вказати інший дефолтний модельний менеджер ми повинні в meta прописати default_manager_name
    published = PublishManager() # вказуємо додатковий прикладний менеджер

    class Meta:

        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def get_absolute_url (self):

        return reverse ('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    def __str__(self):
        return self.title
    

class Comment (models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    name = models.CharField (max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField (auto_now_add=True)
    updated = models.DateTimeField (auto_now=True)
    active = models.BooleanField (default=True)

    class Meta:

        ordering = ['created']

        indexes = [
            models.Index (fields=['created'])
        ]

    def __str__ (self):

        return f'Comment by {self.name} on {self.post}'
    
    