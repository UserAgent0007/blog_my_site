from .forms import EmailPostForm, CommentForm, SearchForm

from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST # декоратор, який вимагає, щоб запит був POST
from django.contrib.postgres.search import SearchVector

# Create your views here.

from .models import Post
from taggit.models import Tag
from django.db.models import Count

class PostListView (ListView):

    context_object_name = 'posts'
    queryset = Post.published.all()
    paginate_by = 3 # повертає у шаблон змінну під назвою page_obj
    template_name = 'blog/post/list.html'

def post_list (request, tag_slug=None):

    post_list = Post.published.all()

    tag = None
    if tag_slug:

        tag = get_object_or_404 (Tag, slug=tag_slug)
        post_list = post_list.filter (tags__in = [tag])

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    
    try:
    
        posts = paginator.page(page_number) # це об єкт page де буде зберігатися ітерована послідовність (list of sth) 
                                            # та номер сторінки з можливістю використання функцій has_previous, has_next,
                                            # number (поточний номер сторінки), next_page_number, previous_page_number
                                            # page_object.paginator.num_pages, page_object.paginator.num_pages
                                            # page_object в даному випадку це posts

    except PageNotAnInteger: # Якщо в запит буде введено щось , що не є цілим числом

        posts = paginator.page (1)
    
    except EmptyPage: # якщо за межіми діапазона доступних сторінок

        posts = paginator.page(paginator.num_pages)

    context = {
        'posts':posts,
        'tag':tag
    }

    return render(request, 'blog/post/list.html', context)

def post_detail (request, year, month, day, post):

    # try:
    #     post = Post.objects.get (id = id)
    
    # except Post.DoesNotExist:
    #     raise Http404 ('No post found')

    post = get_object_or_404 (Post, status = Post.Status.PUBLISHED, publish__year = year, publish__month = month, publish__day = day, slug = post)
    
    comments = post.comments.filter (active = True)
    form = CommentForm ()

    post_tags_ids = post.tags.values_list ('id', flat=True) # повертає кортежі зі значеннями заданих полів 
                                                            # (flat = True, вказує щоб повернувся список значень, 
                                                            # а самі значення не були кортежами)
    similar_posts = Post.published.filter (tags__in = post_tags_ids).exclude (id = post.id)
    similar_posts = similar_posts.annotate (same_tags = Count('tags')).order_by ('-same_tags', '-publish')[:4] # оголошуємо нове поле для відфільтрованого об єкта queryset

    return render (request, 'blog/post/detail.html', {'post':post, 'comments': comments, 'form': form, 'similar_posts':similar_posts})

def post_share (request, post_id):

    post = get_object_or_404 (Post, id = post_id, status = Post.Status.PUBLISHED)
    
    sent = False
    if request.method == 'POST':

        form = EmailPostForm (request.POST)

        if form.is_valid ():

            cd = form.cleaned_data

            post_url = request.build_absolute_uri(post.get_absolute_url()) # повертає абсолютну адресу з портом, всіма протоколами
            # потрібне для того, щоб формувати повну адресу, яка використовуватиметься в листах та інших місцях , 
            # де потрібна абсолютна адреса, а не відносна
    
            subject = (f"{cd['name']} recomends you read "
                       f"{post.title}"
            )
            
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )

            send_mail(subject, message, None, [cd['to']])
            sent = True
    else:

        form = EmailPostForm

    return render (request, 'blog/post/share.html', {'form': form, 'post': post, 'sent':sent})

@require_POST # декоратор, який вимагає, щоб запит був POST
def post_comment (request, post_id):

    post = get_object_or_404 (Post, id = post_id, status = Post.Status.PUBLISHED)
    comment = None

    form = CommentForm (data = request.POST)
    
    if form.is_valid ():

        comment = form.save(commit = False) # без збереження у базу даних
        comment.post = post
        comment.save()

    context = {
        'post': post,
        'form': form,
        'comment': comment
    }

    return render (request, 'blog/post/comment.html', context)

def post_search (request):

    form = SearchForm ()
    query = None
    results = []

    if 'query' in request.GET:

        form = SearchForm (request.GET)
        
        if form.is_valid():

            query = form.cleaned_data['query']
            results = (
                Post.published.annotate (search = SearchVector('title', 'body')).filter (search=query)
            )
    return render (
                    request, 
                    'blog/post/search.html', 
                    {
                        'form': form, 
                        'query': query, 
                        'results': results
                    }
                )
