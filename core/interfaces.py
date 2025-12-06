from abc import ABC, abstractmethod
from typing import List, Any


class ICartRepository(ABC):
    @abstractmethod
    def get_cart_items(self, user) -> List[Any]: pass

    @abstractmethod
    def add_item(self, user, product_id: int, quantity: int) -> None: pass

    @abstractmethod
    def update_item_qty(self, user, product_id: int, quantity: int) -> None: pass

    @abstractmethod
    def remove_item(self, user, product_id: int) -> None: pass

    @abstractmethod
    def remove_product_from_all_carts(self, product): pass


class IProductRepository(ABC):
    @abstractmethod
    def get_all(self) -> Any: pass

    @abstractmethod
    def get_product(self, product_id) -> Any: pass

    @abstractmethod
    def save_product(self, product) -> None: pass

    @abstractmethod
    def delete_product(self, product_id): pass

class ICustomerRepository(ABC):
    @abstractmethod
    def get_customer(self, user) -> Any: pass

class ICategoryRepository(ABC):
    @abstractmethod
    def get_all(self) -> Any: pass

    @abstractmethod
    def get_category(self, category_id) -> Any: pass

    @abstractmethod
    def save_category(self, category) -> None: pass


class IAddressRepository(ABC):
    @abstractmethod
    def get_user_addresses(self, user) -> List[Any]: pass

    @abstractmethod
    def get_address(self, user, address_id) -> Any: pass

    @abstractmethod
    def save_address(self, address) -> None: pass

    @abstractmethod
    def delete_address(self, address) -> None: pass

class IOrderRepository(ABC):
    @abstractmethod
    def address_has_orders(self, address) -> bool:
        pass

    @abstractmethod
    def product_has_orders(self, product) -> bool:
        pass

    @abstractmethod
    def get_user_orders(self, user) -> Any: pass

    @abstractmethod
    def get_order_items(self, order) -> List[Any]: pass

    @abstractmethod
    def get_all(self) -> Any: pass

    @abstractmethod
    def get_order(self, pk) -> None: pass

    @abstractmethod
    def save_order(self, order) -> None: pass

# --- Services ---

class ICartService(ABC):
    @abstractmethod
    def get_cart_details(self, user) -> dict: pass

    @abstractmethod
    def add_product(self, user, product_id: int, quantity: int) -> None: pass

    @abstractmethod
    def update_quantity(self, user, product_id: int, quantity: int) -> None: pass

    @abstractmethod
    def remove_product(self, user, product_id: int) -> None: pass

    @abstractmethod
    def get_checkout_data(self, user) -> dict: pass

    @abstractmethod
    def remove_product_from_all_carts(self, product): pass


class IProductService(ABC):
    @abstractmethod
    def get_products_for_display(self) -> Any: pass

    @abstractmethod
    def get_product(self, product_id) -> Any: pass

    @abstractmethod
    def get_product_inventory(self, product_id) -> int: pass  # Added this

    @abstractmethod
    def save_product(self, product) -> None: pass

    @abstractmethod
    def delete_product(self, product_id): pass


class ICategoryService(ABC):
    @abstractmethod
    def get_categories(self) -> Any: pass

    @abstractmethod
    def get_category(self, category_id) -> Any: pass

    @abstractmethod
    def save_category(self, category) -> None: pass


class IAddressService(ABC):
    @abstractmethod
    def get_user_addresses(self, user) -> List[Any]: pass

    @abstractmethod
    def get_address(self, user, address_id) -> Any: pass

    @abstractmethod
    def save_address(self, user, address) -> None: pass

    @abstractmethod
    def delete_address(self, user, address) -> None: pass

class IOrderService(ABC):
    @abstractmethod
    def is_address_linked_to_order(self, address) -> bool:
        pass

    @abstractmethod
    def is_product_linked_to_order(self, product) -> bool: pass

    @abstractmethod
    def get_user_orders(self, user) -> Any: pass

    @abstractmethod
    def get_all(self) -> Any: pass

    @abstractmethod
    def sent_order(self, pk) -> None: pass

    @abstractmethod
    def complete_order(self, pk) -> None: pass


class ICustomerService(ABC):
    @abstractmethod
    def get_customer(self, user) -> Any: pass