from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book
from .forms import BookForm

def index(request):
    per_page_param = request.GET.get('per_page', '5')
    try:
        per_page = int(per_page_param)
        if per_page <= 0:
            per_page = 5
    except ValueError:
        per_page = 5

    book_list = Book.objects.all().order_by('id')
    paginator = Paginator(book_list, per_page)

    page = request.GET.get('page', 1)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'books': books, 'per_page': per_page})

# Доступно только авторизованным пользователям (как обычным, так и администраторам)
@login_required(login_url='/accounts/login/')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

# Функция для проверки, является ли пользователь администратором
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

# Доступно только администраторам
@user_passes_test(is_admin, login_url='/accounts/login/')
def update_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm(instance=book)
    return render(request, 'update_book.html', {'form': form, 'book': book})

# Доступно только администраторам
@user_passes_test(is_admin, login_url='/accounts/login/')
def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        book.delete()
        return redirect('home')
    return render(request, 'delete_book.html', {'book': book})
