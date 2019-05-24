from django.shortcuts import render, HttpResponse, redirect, reverse, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
import requests
from .models import Books, BookUrls, Likes, ShareUrls
from .form import RegisterForm, LoginForm


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
    msg = request.GET.get('msg', '').strip()
    page_num = request.GET.get('page', 1)
    context = {}

    if not msg:
        context['book_count'] = 0
        return render(request, 'search.html', context)
    books = Books.objects.filter(
        Q(book_name__icontains=msg) | Q(author__icontains=msg))
    pagintor = Paginator(books, 20)

    context['book_count'] = books.count()
    context['books'] = pagintor.get_page(page_num)
    context['msg'] = msg

    return render(request, 'search.html', context)


def author_view(request):
    msg = request.GET.get("msg", '').strip()
    context = {}

    if not msg:
        context['book_count'] = 0
        return render(request, 'search.html', context)
    books = Books.objects.filter(author=msg)

    context['books'] = books
    context['book_count'] = books.count()

    return render(request, 'search.html', context)


def book_view(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    book_urls = BookUrls.objects.filter(book=book_id).order_by('-rate')
    context = {}

    if request.user.is_authenticated:
        is_like = Likes.objects.filter(book=book, user=request.user)
        if is_like:
            context['like'] = True
    context['book'] = book
    context['book_urls'] = book_urls
    if request.COOKIES.get('book' + str(book_id)) != '1':
        print('book' + str(book_id))
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


def support_view(request, url_id):
    book_url = get_object_or_404(BookUrls, id=url_id)
    data = {}
    book_url.support += 1
    rate = book_url.support * 10 / \
        (book_url.support + book_url.against)
    book_url.rate = float('%.1f' % rate)
    book_url.save()
    data['rate'] = book_url.rate
    data['support'] = book_url.support
    return JsonResponse(data)


def against_view(request, url_id):
    book_url = get_object_or_404(BookUrls, id=url_id)
    data = {}
    book_url.against += 1
    rate = book_url.support * 10 / \
        (book_url.support + book_url.against)
    book_url.rate = float('%.1f' % rate)
    book_url.save()
    data['rate'] = book_url.rate
    data['against'] = book_url.against
    return JsonResponse(data)


def share_view(request):
    url = request.GET.get('surl')
    book_id = request.GET.get('book_id')
    book = get_object_or_404(Books, id=book_id)
    data = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    }
    try:
        response = requests.head(url, headers=headers, timeout=4)
    except:
        data['msg'] = '链接不可达'
    else:
        if response.status_code == 200:
            share_url = ShareUrls(book=book, book_url=url)
            share_url.save()
            data['msg'] = '感谢您的分享，我们会尽快核实'
        else:
            data['msg'] = '链接不可达'
    return JsonResponse(data)


def msu_view(request):
    if request.user.is_staff or request.user.is_superuser:
        share_urls = ShareUrls.objects.all()
        page = request.GET.get('page', 1)
        pagintor = Paginator(share_urls, 50)
        context = {}
        context['num'] = share_urls.count()
        context['urls'] = pagintor.get_page(page)
        return render(request, 'manage.html', context)
    else:
        return HttpResponse(status=403)


def addurl_view(request, url_id):
    if request.user.is_staff or request.user.is_superuser:
        url = get_object_or_404(ShareUrls, id=url_id)
        book_urls = BookUrls.objects.filter(book=url.book)
        data = {}
        for book_url in book_urls:
            if url.book_url in book_url.book_url or book_url.book_url in url.book_url:
                url.delete()
                return JsonResponse(data)
        book = BookUrls(book=url.book, book_url=url.book_url)
        book.save()
        url.delete()
        return JsonResponse(data)
    else:
        return HttpResponse(status=403)


def deleteurl_view(request, url_id):
    if request.user.is_staff or request.user.is_superuser:
        url = get_object_or_404(ShareUrls, id=url_id)
        url.delete()
        return JsonResponse({})
    else:
        return HttpResponse(status=403)
