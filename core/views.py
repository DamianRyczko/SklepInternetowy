from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem, Customer, Category, Address, OrderItem, Order
from .filters import ProductFilter  # Importujemy nasz filtr
from .forms import CategoryForm, ProductForm, AddressForm, CardForm, BlikForm
from django.contrib import messages

from .services import CartService, ProductService, CategoryService, AddressService, OrderService, CustomerService
from .repositories import DjangoCartRepository, DjangoProductRepository, DjangoCategoryRepository, \
    DjangoAddressRepository, DjangoOrderRepository, DjangoCustomerRepository

@login_required(login_url='login')
def checkout(request):
    cart_items = None
    addresses = None
    selected_address = None
    customer = Customer.objects.get(user=request.user)

    if request.user.is_authenticated:
        try:
            user_cart = Cart.objects.get(customer=customer)
            cart_items = user_cart.cartitem_set.all()
            addresses = Address.objects.filter(customer=customer)
        except(Customer.DoesNotExist, Cart.DoesNotExist):
            cart_items_count = 0

    if request.method == 'POST':

        if 'clear_address' in request.POST:
            if 'selected_shipping_address' in request.session:
                del request.session['selected_shipping_address']
            return redirect('checkout')

        addr_id = request.POST.get('address_id')
        if addr_id:
            request.session['selected_shipping_address'] = addr_id
            return redirect('checkout')

        if 'card_payment' in request.POST:
            if 'selected_shipping_address' in request.session:
                card_form = CardForm(request.POST)
                if card_form.is_valid():
                    order = Order.objects.create(
                        customer=customer,
                        address=get_object_or_404(Address, id=request.session['selected_shipping_address']),
                        payment_status='C'
                    )
                    for item in cart_items:
                        order_item = OrderItem.objects.create(order=order,
                                                              product=item.product,
                                                              quantity=item.quantity,
                                                              product_name=item.product.title,
                                                              price_on_order=item.product.price)
                        product = Product.objects.get(id=item.product.id)
                        product.inventory = product.inventory - item.quantity
                        product.save()
                        order_item.save()
                        item.delete()
                    return redirect("orders")
                else:
                    messages.error(request, "Invalid card")
            else:
                messages.error(request, "Select Address")

        if 'blik_payment' in request.POST:
            if 'selected_shipping_address' in request.session:
                blik_form = BlikForm(request.POST)
                if blik_form.is_valid():
                    order = Order.objects.create(
                        customer=customer,
                        address=get_object_or_404(Address, id=request.session['selected_shipping_address']),
                        payment_status = 'C'
                    )
                    for item in cart_items:
                        order_item = OrderItem.objects.create(order=order,
                                                              product=item.product,
                                                              quantity=item.quantity,
                                                              product_name=item.product.title,
                                                              price_on_order=item.product.price)
                        product = Product.objects.get(id=item.product.id)
                        product.inventory = product.inventory - item.quantity
                        product.save()
                        order_item.save()
                        item.delete()
                    return redirect("orders")
                else:
                    messages.error(request, "Invalid blik code")
            else:
                messages.error(request, "Select Address")



    session_addr_id = request.session.get('selected_shipping_address')

    if session_addr_id:
        try:
            selected_address = Address.objects.get(id=session_addr_id, customer=customer)
        except Address.DoesNotExist:
            del request.session['selected_shipping_address']


    card_form = CardForm()
    blik_form = BlikForm()

    context = {
        'customer': customer,
        'cart_items': cart_items,
        'addresses': addresses,
        'selected_address': selected_address,
        'card_form': card_form,
        'blik_form': blik_form,
    }
    return render(request, 'core/checkout.html', context)

















#========================================================================================================================================================================
#========================================================================================================================================================================
#========================================================================================================================================================================

#---------------------------- SERVICE FACTORIES ---------------------------
def get_order_service():
    return OrderService(DjangoOrderRepository())

def get_customer_service():
    return CustomerService(DjangoCustomerRepository())

def get_address_service():
    address_repo = DjangoAddressRepository()
    order_service = get_order_service()
    customer_service = get_customer_service()
    return AddressService(
        repo=address_repo,
        order_service=order_service,
        customer_service=customer_service,
    )


def get_product_service():
    product_repo = DjangoProductRepository()
    order_service = get_order_service()
    cart_service = get_cart_service()
    return ProductService(
        repo=product_repo,
        order_service=order_service,
        cart_service=cart_service,
    )

def get_category_service():
    return CategoryService(DjangoCategoryRepository())


def get_cart_service():
    # We instantiate the repo directly
    cart_repo = DjangoCartRepository()

    # We get the other services by calling their factories
    product_repo = DjangoProductRepository()
    address_service = get_address_service()

    # We inject everything into the CartService
    return CartService(
        repo=cart_repo,
        product_repo=product_repo,
        address_service=address_service
    )


#---------------------------- HOME ---------------------------
def home(request):
    service = get_product_service()

    products_queryset = service.get_products_for_display()

    # Nakładamy filtr.
    # request.GET zawiera parametry z URL (np. ?ordering=price)
    product_filter = ProductFilter(request.GET, queryset=products_queryset)

    cart_service = get_cart_service()
    data = cart_service.get_cart_details(request.user)

    # Ważne: do szablonu przekazujemy przefiltrowaną listę (product_filter.qs)
    context = {
        'filter': product_filter,  # Przekazujemy obiekt filtra (by wyświetlić formularz)
        'products': product_filter.qs,  # Przekazujemy posortowane/przefiltrowane produkty
        'cart_items_count': data['count'],
    }

    return render(request, 'core/index.html', context)

#---------------------------- CUSTOMER ---------------------------
@login_required(login_url='login')
def orders(request):
    service = get_order_service()
    order_list = service.get_user_orders(request.user)
    return render(request, 'core/orders.html', {'order_list': order_list})

@login_required(login_url='login')
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            service = get_address_service()
            address = form.save(commit=False)
            service.save_address(request.user, address)
            form.save_m2m()
            return redirect('checkout')
    else:
        form = AddressForm()
    return render(request, 'core/address.html', {'form': form})


@login_required(login_url='login')
def delete_address(request, address_id):
    if request.method == 'POST':
        service = get_address_service()

        address = service.get_address(request.user, address_id)

        if address:
            service.delete_address(request.user, address)
    return redirect('checkout')
#---------------------------- CART ---------------------------
@login_required(login_url='login')
def cart(request):
    service = get_cart_service()
    data = service.get_cart_details(request.user)

    context = {
        'cart_items': data['items'],
        'cart_value': data['total_value'],
    }
    return render(request, 'core/cart.html', context)

@login_required(login_url='login')
def add_to_cart(request, product_id):
    if request.method == 'POST':
        try:
            qty = int(request.POST.get('quantity'))
            get_cart_service().add_product(request.user, product_id, qty)
        except (ValueError, TypeError):
            pass
    return redirect('home')



@login_required(login_url='login')
def update_quantity(request, product_id):
    if request.method == 'POST':
        service = get_cart_service()

        try:
            service.update_quantity(request.user, product_id, int(request.POST.get('quantity')))
        except (ValueError, TypeError):
            # Handle case where quantity isn't a number
            pass

    return redirect('cart')

@login_required(login_url='login')
def delete_from_cart(request, product_id):
    if request.method == 'POST':
        service = get_cart_service()
        service.remove_product(request.user, product_id)

    return redirect('cart')

#---------------------------- EMPLOYEE ---------------------------
def employee_products(request):
    service = get_product_service()
    products = service.get_products_for_display()
    return render(request, 'core/employee_products.html', {'products': products})


def employee_orders(request):
    service = get_order_service()
    orders = service.get_all()
    return render(request, 'core/employee_orders.html', {'orders': orders})

def orders_sent(request, pk):
    service = get_order_service()
    service.sent_order(pk)
    return redirect('employee_orders')


def orders_completed(request, pk):
    service = get_order_service()
    service.complete_order(pk)
    return redirect('employee_orders')


def employee_categories(request):
    service = get_category_service()
    categories = service.get_categories()
    return render(request, 'core/employee_categories.html', {'categories': categories})
def manage_category(request, pk=None):
    service = get_category_service()
    category = service.get_category(pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_obj = form.save(commit=False)

            service.save_category(category_obj)

            # Zapisujemy relacje Many-to-Many
            form.save_m2m()

            return redirect('employee_categories')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'core/category_add.html', {'form': form})

def manage_product(request, pk = None):
    service = get_product_service()
    product = service.get_product(pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            product_obj = form.save(commit=False)
            service.save_product(product_obj)
            form.save_m2m()
            return redirect('employee_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'core/products_add.html', {'form': form})

def delete_product(request, pk):
    if request.method == 'POST':
        service = get_product_service()
        service.delete_product(pk)
    return redirect('employee_products')

