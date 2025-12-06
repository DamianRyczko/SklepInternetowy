from typing import Any
from .models import Product, Cart, CartItem, Customer, Address, Category, Order, OrderItem
from .interfaces import ICartRepository, IProductRepository, ICategoryRepository, IAddressRepository, IOrderRepository, \
    ICustomerRepository
from django.shortcuts import get_object_or_404

class DjangoCartRepository(ICartRepository):
    def _get_cart(self, user):
        customer, _ = Customer.objects.get_or_create(user=user)
        cart, _ = Cart.objects.get_or_create(customer=customer)
        return cart

    def get_cart_items(self, user):
        if not user.is_authenticated: return []
        cart = self._get_cart(user)
        return cart.cartitem_set.select_related('product').all()

    def add_item(self, user, product_id: int, quantity: int) -> None:
        cart = self._get_cart(user)
        product = get_object_or_404(Product, pk=product_id)
        cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 0})
        cart_item.quantity += quantity
        cart_item.save()

    def update_item_qty(self, user, product_id: int, quantity: int) -> None:
        cart = self._get_cart(user)
        product = get_object_or_404(Product, pk=product_id)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            if quantity <= 0:
                cart_item.delete()
            else:
                cart_item.quantity = quantity
                cart_item.save()

    def remove_item(self, user, product_id: int) -> None:
        cart = self._get_cart(user)
        product = get_object_or_404(Product, pk=product_id)
        CartItem.objects.filter(cart=cart, product=product).delete()

    def remove_product_from_all_carts(self, product):
        CartItem.objects.filter(product=product).delete()


class DjangoProductRepository(IProductRepository):
    def get_all(self):
        return Product.objects.all()

    def get_product(self, product_id):
        return get_object_or_404(Product, pk=product_id)

    def save_product(self, product):
        product.save()

    def delete_product(self, product):
        product.delete()


class DjangoCategoryRepository(ICategoryRepository):
    def get_all(self):
        return Category.objects.all()

    def get_category(self, category_id):
        return get_object_or_404(Category, pk=category_id)

    def save_category(self, category):
        category.save()


class DjangoAddressRepository(IAddressRepository):
    def get_user_addresses(self, user):
        customer, _ = Customer.objects.get_or_create(user=user)
        return Address.objects.filter(customer=customer)

    def get_address(self, user, address_id):
        return get_object_or_404(Address, pk=address_id)

    def save_address(self, address):
        address.save()

    def delete_address(self, address):
        address.delete()

class DjangoOrderRepository(IOrderRepository):
    def address_has_orders(self, address) -> bool:
        return Order.objects.filter(address=address).exists()

    def product_has_orders(self, product) -> bool:
        return OrderItem.objects.filter(product=product).exists()

    def get_user_orders(self, user):
        customer, _ = Customer.objects.get_or_create(user=user)
        return Order.objects.filter(customer=customer)

    def get_order_items(self, order):
        return OrderItem.objects.filter(order=order).all()

    def get_all(self) -> Any:
        return Order.objects.all()

    def get_order(self, order_id):
        return get_object_or_404(Order, pk=order_id)

    def save_order(self, order):
        order.save()



class DjangoCustomerRepository(ICustomerRepository):
    def get_customer(self, user):
        return get_object_or_404(Customer, user=user)