from django.shortcuts import render,HttpResponse
from .models import Books, Sources, Likes


def index(request):
    books = Books.objects.all()
    print(books)
    return HttpResponse('sadhjasd')


