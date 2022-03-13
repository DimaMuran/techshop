import decimal
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Address, Cart, Category, Order, Product
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def home(request):
    categories = Category.objects.filter(is_active=True, is_featured=True)[:3]
    products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request,'store/index.html',context)

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
    if item_already_in_cart:
        cp = get_object_or_404(Cart, product=product_id, user=user)
        cp.quantity += 1
        cp.save()
    else:
        Cart(user=user, product=product).save()

    return redirect('cart')


@login_required
def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, 'Product removed from Cart.')
    return redirect('cart')


@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity +=1
        cp.save()
    return redirect('cart')


@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()

    return redirect('cart')


@login_required
def cart(request):
    user = request.user
    cart_products = Cart.objects.filter(user=user)

    amount = decimal.Decimal(0)
    shipping_amount = decimal.Decimal(10)

    cp = [p for p in Cart.objects.all() if p.user==user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount
        
    addresses = Address.objects.filter(user=user)

    context = {
        'cart_products': cart_products,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': amount + shipping_amount,
        'addresses': addresses,
    }
    return render(request, 'store/cart.html', context)


@login_required
def checkout(request):
    user = request.user
    address_id = request.GET.get('address')

    address = get_object_or_404(Address, id=address_id)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        Order(user=user, address=address, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')


@login_required
def orders(request):
    all_orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request,'store/orders.html', {'orders': all_orders})


def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.exclude(id=product.id).filter(is_active=True, category=product.category)
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/detail.html', context)


def all_categories(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'store/categories.html', {'categories': categories})


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(is_active=True, category=category)
    categories = Category.objects.filter(is_active=True)
    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/category_products.html', context)


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations! Registration Successful!')
            form.save()
        return render(request, 'account/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect') 
            return redirect('login')
        

@login_required
def logoutUser(request):
    logout(request)
    return redirect('home')
