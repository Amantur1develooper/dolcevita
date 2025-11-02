# menu/cart.py
from decimal import Decimal
from django.conf import settings
from core.models import Product

CART_SESSION_KEY = "cart"  # {product_id: qty}

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if cart is None:
            cart = {}
            self.session[CART_SESSION_KEY] = cart
        self.cart = cart

    def add(self, product_id: int, qty: int = 1, replace: bool = False):
        pid = str(product_id)
        if pid not in self.cart:
            self.cart[pid] = 0
        self.cart[pid] = qty if replace else self.cart[pid] + qty
        if self.cart[pid] <= 0:
            self.cart.pop(pid, None)
        self.save()

    def remove(self, product_id: int):
        self.cart.pop(str(product_id), None)
        self.save()

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def __len__(self):
        return sum(self.cart.values())

    def items_detailed(self):
        """Возвращает объекты блюд + qty + сумма по позиции."""
        pids = [int(pid) for pid in self.cart.keys()]
        products = Product.objects.in_bulk(pids)
        for pid, qty in self.cart.items():
            obj = products.get(int(pid))
            if not obj:
                # если блюдо удалено из БД — убрать из корзины
                self.remove(pid)
                continue
            line_total = (obj.price or Decimal("0")) * qty
            yield {
                "product": obj,
                "qty": qty,
                "line_total": line_total,
            }

    def total(self):
        return sum(i["line_total"] for i in self.items_detailed())
