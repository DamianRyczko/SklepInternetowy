from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem, Customer, Category
from .filters import ProductFilter  # Importujemy nasz filtr
from .forms import CategoryForm, ProductForm
def home(request):
    # Pobieramy wszystkie produkty
    products_list = Product.objects.all()

    # Nakładamy filtr.
    # request.GET zawiera parametry z URL (np. ?ordering=price)
    product_filter = ProductFilter(request.GET, queryset=products_list)

    cart_items_count = 0

    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            user_cart = Cart.objects.get(customer=customer)
            cart_items = user_cart.cartitem_set.all()
            for item in cart_items:
                cart_items_count += item.quantity
        except(Customer.DoesNotExist, Cart.DoesNotExist):
            cart_items_count = 0

    # Ważne: do szablonu przekazujemy przefiltrowaną listę (product_filter.qs)
    context = {
        'filter': product_filter,  # Przekazujemy obiekt filtra (by wyświetlić formularz)
        'products': product_filter.qs,  # Przekazujemy posortowane/przefiltrowane produkty
        'cart_items_count': cart_items_count,
    }

    return render(request, 'core/index.html', context)

@login_required(login_url='login')
def cart(request):
    cart_items = None
    cart_value = 0
    customer = Customer.objects.get(user=request.user)
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            user_cart = Cart.objects.get(customer=customer)
            cart_items = user_cart.cartitem_set.all()
        except(Customer.DoesNotExist, Cart.DoesNotExist):
            cart_items_count = 0

    for item in cart_items:
        cart_value += item.quantity * item.product.price
    context = {
        'customer': customer,
        'cart_items': cart_items,
        'cart_value': cart_value,
    }
    return render(request, 'core/cart.html', context)
@login_required(login_url='login')
def checkout(request):
    cart_items = None
    customer = Customer.objects.get(user=request.user)
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            user_cart = Cart.objects.get(customer=customer)
            cart_items = user_cart.cartitem_set.all()
        except(Customer.DoesNotExist, Cart.DoesNotExist):
            cart_items_count = 0
    context = {
        'customer': customer,
        'cart_items': cart_items,
    }
    return render(request, 'core/checkout.html',context)
@login_required(login_url='login')
def orders(request):
    return render(request, 'core/orders.html')

@login_required(login_url='login')
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        customer, created = Customer.objects.get_or_create(user=request.user)
        user_cart, created = Cart.objects.get_or_create(customer=customer)
        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product, defaults={'quantity': 0})
        try:
            cart_item.quantity += int(request.POST.get('quantity'))
        except (ValueError, TypeError):
            # Handle case where quantity isn't a number
            return redirect('home')

        if cart_item.quantity > product.inventory:
            cart_item.quantity = product.inventory
        cart_item.save()
        return redirect('home')
    return redirect('home')

@login_required(login_url='login')
def update_quantity(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        customer, created = Customer.objects.get_or_create(user=request.user)
        user_cart, created = Cart.objects.get_or_create(customer=customer)
        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product, defaults={'quantity': 0})

        try:
            cart_item.quantity = int(request.POST.get('quantity'))
        except (ValueError, TypeError):
            # Handle case where quantity isn't a number
            return redirect('cart')

        if cart_item.quantity > product.inventory:
            cart_item.quantity = product.inventory
        if cart_item.quantity < 0:
            cart_item.quantity = 0

        if cart_item.quantity == 0:
            cart_item.delete()
        else:
            cart_item.save()

        return redirect('cart')
    return redirect('cart')
    return None

@login_required(login_url='login')
def delete_from_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        customer, created = Customer.objects.get_or_create(user=request.user)
        user_cart, created = Cart.objects.get_or_create(customer=customer)
        cart_item = CartItem.objects.get(cart=user_cart, product=product)

        cart_item.delete()
        return redirect('cart')
    return redirect('cart')


def employee_orders(request):
    return render(request, 'core/employee_orders.html')


def employee_categories(request):
    categories = Category.objects.all()
    return render(request, 'core/employee_categories.html', {'categories': categories})


def employee_products(request):
    products = Product.objects.all()
    return render(request, 'core/employee_products.html', {'products': products})


def manage_category(request, pk = None):
    if pk:
        category = get_object_or_404(Category, pk=pk)
    else:
        category = None
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('employee_categories')
    else:

        form = CategoryForm(instance=category)
    return render(request, 'core/category_add.html', {'form': form})


def manage_product(request, pk = None):
    if pk:
        product = get_object_or_404(Product, pk=pk)
    else:
        product = None
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            return redirect('employee_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'core/products_add.html', {'form': form})