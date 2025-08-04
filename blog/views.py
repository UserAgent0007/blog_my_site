from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator

# Create your views here.

from .models import Post

def post_list (request):

    post_list = Post.published.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number) # це об єкт page де буде зберігатися ітерована послідовність (list of sth) 
                                        # та номер сторінки з можливістю використання функцій has_previous, has_next,
                                        # number (поточний номер сторінки), next_page_number, previous_page_number
                                        # page_object.paginator.num_pages, page_object.paginator.num_pages
                                        # page_object в даному випадку це posts

    context = {
        'posts':posts
    }

    return render(request, 'blog/post/list.html', context)

def post_detail (request, year, month, day, post):

    # try:
    #     post = Post.objects.get (id = id)
    
    # except Post.DoesNotExist:
    #     raise Http404 ('No post found')

    post = get_object_or_404 (Post, status = Post.Status.PUBLISHED, publish__year = year, publish__month = month, publish__day = day, slug = post)
    
    return render (request, 'blog/post/detail.html', {'post':post})