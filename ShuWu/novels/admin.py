from django.contrib import admin
from . models import Books


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    search_fields = ('book_name', 'author')
    list_display = ('book_name', 'author')
