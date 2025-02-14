# booksapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Book
from .forms import BookForm


def index(request):
    # Get the desired items per page from query parameters; default to 5 if not provided or invalid.
    per_page_param = request.GET.get('per_page', '5')
    try:
        per_page = int(per_page_param)
        if per_page <= 0:
            per_page = 5
    except ValueError:
        per_page = 5

    # Fetch all books and order them (you can change the ordering as needed)
    book_list = Book.objects.all().order_by('id')
    paginator = Paginator(book_list, per_page)

    # Get the current page number from query parameters; default to 1.
    page = request.GET.get('page', 1)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    # Pass the current per_page value to the template to maintain the selection.
    return render(request, 'index.html', {'books': books, 'per_page': per_page})


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home after saving
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})


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

# booksapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm

# ... (other views)

def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        book.delete()
        return redirect('home')
    return render(request, 'delete_book.html', {'book': book})
