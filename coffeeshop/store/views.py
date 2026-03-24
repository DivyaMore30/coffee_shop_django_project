from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render

from .models import Product, Cart
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

#this function displays the list of products
def product(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

#this function displays the details of a product
def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product_detail.html', {'product': product})




@login_required
def add_to_cart(request, product_id): #this function adds a product to the database
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def increase_quantity(request, cart_id):
    cart_item = Cart.objects.get(id=cart_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
def decrease_quantity(request, cart_id):
    cart_item = Cart.objects.get(id=cart_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

@login_required
def remove_item(request, cart_id):
    cart_item = Cart.objects.get(id=cart_id)
    cart_item.delete()
    return redirect('cart')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user = User.objects.create_user(username = username, password = password, email = email, first_name = first_name, last_name = last_name)
        return redirect("login")
    return render(request, 'register.html')


#login_view

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "login.html")
# logout_view
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("login")