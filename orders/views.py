from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from booksapp.models import Book
from .models import Cart, CartItem, Order, OrderItem

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    total = cart.total_cost()
    return render(request, 'orders/cart.html', {'cart': cart, 'total': total})

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CartItem

@login_required
def remove_from_cart(request, item_id):
    # Находим элемент корзины, принадлежащий текущему пользователю
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        item.delete()
    return redirect('view_cart')


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        return redirect('view_cart')
    total = cart.total_cost()
    order = Order.objects.create(user=request.user, total_cost=total)
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            book=item.book,
            quantity=item.quantity,
            price=item.book.price
        )
    # Очистка корзины
    cart.items.all().delete()
    return redirect('order_history')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'orders/order_history.html', {'orders': orders})
