from typing import Any

from .interfaces import ICartRepository, IProductRepository, ICartService, \
    IProductService, ICategoryService, ICategoryRepository, IAddressService, IAddressRepository, IOrderService, \
    IOrderRepository, ICustomerService, ICustomerRepository


class ProductService(IProductService):
    def __init__(self, repo: IProductRepository, order_service: IOrderService, cart_service: ICartService):
        self.repo = repo
        self.order_service = order_service
        self.cart_service = cart_service

    def get_products_for_display(self):
        return self.repo.get_all()

    def get_product(self, product_id):
        if product_id is None: return None
        return self.repo.get_product(product_id)

    def get_product_inventory(self, product_id) -> int:
        product = self.repo.get_product(product_id)
        return getattr(product, 'inventory', 0)

    def save_product(self, product):
        self.repo.save_product(product)

    def delete_product(self, product_id):
        product = self.repo.get_product(product_id)
        if not product:
            return

        self.cart_service.remove_product_from_all_carts(product)

        is_linked_to_order = self.order_service.is_product_linked_to_order(product)

        if is_linked_to_order:
            product.is_active = False
            self.repo.save_product(product)
        else:
            self.repo.delete_product(product)


class OrderService(IOrderService):
    def __init__(self, repo: IOrderRepository):
        self.repo = repo

    def is_address_linked_to_order(self, address) -> bool:
        return self.repo.address_has_orders(address)

    def is_product_linked_to_order(self, product) -> bool:
        return self.repo.product_has_orders(product)

    def get_user_orders(self, user):
        orders =  self.repo.get_user_orders(user)

        formatted_data = []

        for order in orders:
            order_items = self.repo.get_order_items(order)

            entry = {
                "order_details": order,
                "items": order_items
            }

            formatted_data.append(entry)

        return formatted_data

    def get_all(self):
        return self.repo.get_all()

    def sent_order(self, pk):
        order = self.repo.get_order(pk)
        order.order_status = 'S'
        self.repo.save_order(order)

    def complete_order(self, pk):
        order = self.repo.get_order(pk)
        order.order_status = 'C'
        self.repo.save_order(order)


class CustomerService(ICustomerService):
    def __init__(self, repo: ICustomerRepository):
        self.repo = repo

    def get_customer(self, user):
        return self.repo.get_customer(user)

class AddressService(IAddressService):
    def __init__(self, repo: IAddressRepository, order_service: IOrderService, customer_service: ICustomerService):
        self.repo = repo
        self.order_service = order_service
        self.customer_service = customer_service

    def get_user_addresses(self, user):
        return self.repo.get_user_addresses(user)

    def get_address(self, user, address_id):
        return self.repo.get_address(user, address_id)

    def save_address(self, user, address):
        address.customer = self.customer_service.get_customer(user)
        self.repo.save_address(address)

    def delete_address(self, user, address):

        is_linked = self.order_service.is_address_linked_to_order(address)

        if is_linked:
            address.is_active = False
            self.repo.save_address(address)
        else:
            self.repo.delete_address(address)


class CartService(ICartService):
    def __init__(self, repo: ICartRepository,
                 product_repo: IProductRepository,  # CHANGED: Depend on Repo, not Service
                 address_service: IAddressService):
        self.repo = repo
        self.product_repo = product_repo  # CHANGED
        self.address_service = address_service

    def get_cart_details(self, user):
        items = self.repo.get_cart_items(user)
        total_val = sum(item.quantity * item.product.price for item in items)
        count = sum(item.quantity for item in items)
        return {
            'items': items,
            'total_value': total_val,
            'count': count
        }

    def add_product(self, user, product_id, quantity):
        self.repo.add_item(user, product_id, quantity)

    def update_quantity(self, user, product_id, quantity):


        product = self.product_repo.get_product(product_id)
        inventory = getattr(product, 'inventory', 0)

        final_qty = min(quantity, inventory)
        self.repo.update_item_qty(user, product_id, final_qty)

    def remove_product(self, user, product_id):
        self.repo.remove_item(user, product_id)

    def remove_product_from_all_carts(self, product):
        self.repo.remove_product_from_all_carts(product)

    def get_checkout_data(self, user):
        cart_data = self.get_cart_details(user)
        addresses = self.address_service.get_user_addresses(user)

        return {
            'cart_items': cart_data['items'],
            'cart_value': cart_data['total_value'],
            'addresses': addresses
        }


class CategoryService(ICategoryService):
    def __init__(self, repo: ICategoryRepository):
        self.repo = repo

    def get_categories(self):
        return self.repo.get_all()

    def get_category(self, category_id):
        if category_id is None: return None
        return self.repo.get_category(category_id)

    def save_category(self, category):
        self.repo.save_category(category)