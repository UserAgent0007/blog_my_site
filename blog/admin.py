from django.contrib import admin
from .models import Post, Comment
# Register your models here.

# admin.site.register (Post)

@admin.register (Post)
class PostAdmin (admin.ModelAdmin):

    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {
        'slug' : ('title', )
    } # Заповнення полів на основі попередньо введених інших полів (це має бути словник , 
      # де ключ поле яке має автоматично заповнюватися, а значення - кортеж з попередніми заповненими полями)
    raw_id_fields = ['author'] # створення пошукового віджету для полів, які є ForeignKey, щоб не вибирати з величезного випадного списку
    date_hierarchy = 'publish' # дозволяє робити фільтр по датам (ієрархія)
    ordering = ['status', 'publish'] # впорядкування за вказаними полями
    show_facets = admin.ShowFacets.ALWAYS # показати кількість об'єктів для кожного фільтра (фасети)

@admin.register (Comment)
class CommentAdmin (admin.ModelAdmin):
    
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']