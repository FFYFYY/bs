from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import Books, BookUrls, Likes
from django.contrib.auth.models import User
from .form import RegisterForm, LoginForm
from django.contrib.auth import logout, login, authenticate
from django.db.models import Q


def index_view(request):
    books = Books.objects.all()
    context = {
        'books': books,
    }
    return render(request, 'index.html', context)


def search_view(request):
    msg = request.POST.get("msg").strip()
    # sources = Sources.objects.filter(Q(book__icontains=msg))
    # for i in sources:
    #     print(i)
    return HttpResponse(msg)


def novel_view(request):
    pass


def like_view(request):
    pass


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
