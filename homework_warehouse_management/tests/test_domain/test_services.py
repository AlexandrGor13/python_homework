import pytest
from domain.services import WarehouseService
from domain.models import Product, Order
from domain.repositories import ProductRepository, OrderRepository

@pytest.fixture
def product_repository():
    class InMemoryProductRepository(ProductRepository):
        def __init__(self):
            self.products = []

        def add(self, product: Product):
            if not product.id:
                product.id = len(self.products) + 1
            self.products.append(product)

        def get(self, product_id: int):
            product = [product for product in self.products if product.id == product_id]
            return product[0] if product else None

        def list(self):
            return self.products

    return InMemoryProductRepository()


@pytest.fixture
def order_repository():
    class InMemoryOrderRepository(OrderRepository):
        def __init__(self):
            self.orders = []

        def add(self, order: Order):
            if not order.id:
                order.id = len(self.orders) + 1
            self.orders.append(order)

        def get(self, order_id: int):
            order = [order for order in self.orders if order.id == order_id]
            return order[0] if order else None

        def list(self):
            return self.orders

    return InMemoryOrderRepository()


def test_create_product(product_repository):
    service = WarehouseService(product_repository, None)
    name = 'Test Product'
    quantity = 10
    price = 99.99

    result = service.create_product(name, quantity, price)
    assert isinstance(result, Product)
    assert result.name == name
    assert result.quantity == quantity
    assert result.price == price
    assert product_repository.get(1) == result
    assert len(product_repository.list()) == 1


def test_create_order(product_repository, order_repository):
    service = WarehouseService(product_repository, order_repository)
    p1 = Product(id=1, name='Product A', quantity=5, price=10.0)
    p2 = Product(id=2, name='Product B', quantity=3, price=15.0)
    product_repository.add(p1)
    product_repository.add(p2)

    result = service.create_order([p1, p2])

    assert isinstance(result, Order)
    assert len(result.products) == 2
    assert result.products[0].name == 'Product A'
    assert result.products[1].name == 'Product B'
    assert order_repository.get(1) == result
    assert len(order_repository.list()) == 1