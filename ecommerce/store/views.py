from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Product, Category, Cart, Order,  OrderItem
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.shortcuts import redirect





def home(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    # 🔍 base products
    products = Product.objects.all()

    # 🔍 search filter
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # 🟢 category filter (NEW)
    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()

    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
    else:
        cart_count = 0

    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories,
        'cart_count': cart_count
    })

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )


    if not created:
        cart_item.quantity += 1

        

    else:
        cart_item.quantity = 1

    cart_item.save()

    return redirect('cart')



def cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

def increase_quantity(request, cart_id):
    item = Cart.objects.get(id=cart_id)

    item.quantity += 1
    item.save()

    return redirect('cart')


def decrease_quantity(request, cart_id):
    item = Cart.objects.get(id=cart_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')


def remove_from_cart(request, cart_id):
    item = get_object_or_404(Cart, id=cart_id, user=request.user)
    item.delete()
    return redirect('cart')


# 👤 REGISTER


def register(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    else:
        form = UserCreationForm()

    # add bootstrap styling (ONLY ONCE)
    for field in form.fields.values():
        field.widget.attrs.update({
            'class': 'form-control',
            'placeholder': field.label
        })

    return render(request, 'store/register.html', {'form': form})

# 🧾 CHECKOUT

def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })

# 📦 PLACE ORDER

def place_order(request):
    if request.method == "POST":

        address = request.POST.get('address')

        cart_items = Cart.objects.filter(user=request.user)

        if not cart_items.exists():
            return redirect('cart')

        # 1. calculate total FIRST
        total = 0
        for item in cart_items:
            total += item.product.price * item.quantity

        # 2. create order with correct total
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            address=address,
            status='Pending'
        )

        # 3. create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # 4. clear cart
        cart_items.delete()

        return render(request, 'store/success.html', {'order': order})
        
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)

    return render(request, 'store/product_detail.html', {
        'product': product
    })

def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')

    return render(request, 'store/order_history.html', {
        'orders': orders
    })


def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)

    return render(request, 'store/order-details.html', {
        'order': order,
        'items': items
    })


def user_logout(request):
    logout(request)
    return redirect('home')
