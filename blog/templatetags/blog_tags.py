from django import template
from ..models import Post
from django.db.models import Count

register = template.Library() # використовується для реєстрації нових шаблонних тегів і фільтрів додатка

@register.simple_tag # simpletag обробляє дані і поверта рядковий літерал (для simpletag можна прописати name="..." і шаблон так і називатиметься)
def total_posts (): 

    return Post.published.count()

@register.inclusion_tag ('blog/post/latest_posts.html') # обробляє данні і повертає промальований шаблон (потрібно вказати шлях до шаблону, який буде малюватися)
def show_latest_posts (count = 5):
    latest_posts = Post.published.order_by ('-publish')[:count]
    
    return {'latest_posts':latest_posts}


@register.simple_tag
def get_most_commented_posts (count = 5):

    return Post.published.annotate(total_comments = Count('comments')).order_by('-total_comments')[:count]