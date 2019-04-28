from django.shortcuts import render, HttpResponse, redirect, reverse, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from .models import Books, BookUrls, Likes
from django.contrib.auth.models import User
from .form import RegisterForm, LoginForm
from django.core.cache import cache
from django.http import JsonResponse
from django.db.models import Q


def index_view(request):
    context = {}
    if request.user.is_authenticated:
        like_books = Likes.objects.filter(user=request.user)
        context['books'] = like_books

    hot_search_novels = cache.get('hot_search_novels')
    if not hot_search_novels:
        hot_search_novels = Books.objects.all().order_by('-searches')[:30]
        cache.set('hot_search_novels', hot_search_novels, 3600)

    context['hot_search_novels'] = hot_search_novels
    return render(request, 'index.html', context)


def search_view(request):
    msg = request.GET.get("msg").strip()
    context = {}
    context['book_count'] = 0
    if not msg:
        return render(request, 'search.html', context)
    books = Books.objects.filter(
        Q(book_name__icontains=msg) | Q(author__icontains=msg))
    book_count = books.count()
    if book_count < 500:
        context['books'] = books
        context['book_count'] = book_count
    else:
        context['book_count'] = 0
    return render(request, 'search.html', context)


def author_view(request):
    msg = request.GET.get("msg").strip()
    context = {}
    if not msg:
        context['book_count'] = 0
        return render(request, 'search.html', context)
    books = Books.objects.filter(author=msg)
    book_count = books.count()
    context['books'] = books
    context['book_count'] = book_count
    return render(request, 'search.html', context)


def book_view(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    book_urls = BookUrls.objects.filter(book=book_id)
    context = {}
    if request.user.is_authenticated:
        is_like = Likes.objects.filter(book=book, user=request.user)
        if is_like:
            context['like'] = "取消收藏"
        else:
            context['like'] = "加入书架"
    context['book'] = book
    context['book_urls'] = book_urls
    book.searches += 1
    book.save()
    return render(request, 'book.html', context)


def like_view(request, book_id):
    data = {}
    if request.user.is_authenticated:
        book = get_object_or_404(Books, id=book_id)
        is_like = Likes.objects.filter(book=book, user=request.user)
        if is_like:
            is_like.delete()
            data['like'] = False
        else:
            like = Likes(book=book, user=request.user)
            like.save()
            data['like'] = True
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(request.GET.get('from', reverse('books:index')))


def register_view(request):
    # 判断用户是否已经登录
    if request.user.is_authenticated:
        return redirect(request.GET.get('from', reverse('books:index')))
    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(
                username=username, password=password)
            user.save()
            authenticated_user = authenticate(
                username=username,
                password=password,
            )
            login(request, authenticated_user)
            return redirect(request.GET.get('from', reverse('books:index')))
    context = {'form': form}
    return render(request, 'register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get('from', reverse('books:index')))
    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return redirect(request.GET.get('from', reverse('books:index')))
    context = {'form': form}
    return render(request, 'login.html', context)
