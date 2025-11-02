# menu/cart.py
from decimal import Decimal
from django.conf import settings
from core.models import Product
from decimal import Decimal

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
        
    def total(self) -> Decimal:
        """Общая сумма корзины (Decimal)."""
        return sum(item["line_total"] for item in self.items_detailed())

    def __len__(self):
        """Количество единиц товара в корзине."""
        return sum(int(qty) for qty in self.cart.values())
    # def __len__(self):
    #     return sum(self.cart.values())

    

    def items_detailed(self):
        """
        Возвращает итератор по позициям корзины с обогащением объектами Product.
        Без изменения словаря во время итерации.
        """
        # делаем снимок текущего словаря, чтобы не словить RuntimeError
        snapshot_items = list(self.cart.items())  # [(pid_str, qty), ...]
    
        # заранее подтягиваем продукты одним запросом
        pids = [int(pid_str) for pid_str, _ in snapshot_items]
        products = Product.objects.in_bulk(pids)  # {pid:int -> Product}
    
        to_delete = []
    
        for pid_str, qty in snapshot_items:
            try:
                qty = int(qty)
            except (TypeError, ValueError):
                to_delete.append(pid_str)
                continue
            if qty <= 0:
                to_delete.append(pid_str)
                continue

            pid = int(pid_str)
            obj = products.get(pid)
            if not obj:
                # блюдо удалено/неактивно — отметим на удаление после цикла
                to_delete.append(pid_str)
                continue

        line_total = (obj.price or Decimal("0")) * qty
        yield {
            "product": obj,
            "qty": qty,
            "line_total": line_total,
        }

        # чистим корзину уже после обхода
        if to_delete:
            for k in to_delete:
                self.cart.pop(k, None)
            self.save()

        def total(self):
            return sum(i["line_total"] for i in self.items_detailed())


