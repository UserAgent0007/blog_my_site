from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap (Sitemap):

    changefreq = 'weekly' # частота зміни сторінок постів
    priority = 0.9 # важливість сторінок

    def items (self): # повертає об єкт QuerySet, який потім включається в карту сайту 
                      # за замовчуванням посилання на пости беруться із get_absolute_url
        return Post.published.all()
    
    def lastmod (self, obj): # бере кожний об єкт Post із QuerySet, який отримується методом items, і повертає останнє оновлення для цього поста

        return obj.updated