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

    # core/cart.py
    def add(self, product_id: int, qty: int = 1, replace: bool = False):
        pid = str(int(product_id))
        qty = int(qty)
        current = int(self.cart.get(pid, 0))
        self.cart[pid] = qty if replace else current + qty
        if self.cart[pid] <= 0:
            self.cart.pop(pid, None)
        self.save()

    # def add(self, product_id: int, qty: int = 1, replace: bool = False):
    #     pid = str(int(product_id))
    #     qty = int(qty)
    #     current = int(self.cart.get(pid, 0))
    #     self.cart[pid] = qty if replace else current + qty
    #     if self.cart[pid] <= 0:
    #         self.cart.pop(pid, None)
    #     self.save()


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
        Итератор по позициям корзины:
        - без изменения self.cart во время обхода;
        - с жёсткой валидацией pid/qty;
        - без обращения к obj, если его нет (исключает UnboundLocalError).
        """
        snapshot = list(self.cart.items())  # [(pid_str, qty_str), ...]
        if not snapshot:
            return iter(())  # пустой итератор

        valid_triplets = []  # (pid_str, pid_int, qty_int)
        to_delete = []

        # 1) Валидация id/qty
        for pid_str, qty in snapshot:
            try:
                pid = int(pid_str)
                q = int(qty)
            except (TypeError, ValueError):
                to_delete.append(pid_str)
                continue
            if q <= 0:
                to_delete.append(pid_str)
                continue
            valid_triplets.append((pid_str, pid, q))

        if not valid_triplets:
            # подчистим и вернём пусто
            if to_delete:
                for k in to_delete:
                    self.cart.pop(k, None)
                self.save()
            return iter(())

        # 2) Подтянем продукты одним запросом
        pids = [pid for _, pid, _ in valid_triplets]
        products = Product.objects.in_bulk(pids)  # {pid_int: Product}

        # 3) Генерация позиций
        def _gen():
            local_to_delete = []
            for pid_str, pid, q in valid_triplets:
                obj = products.get(pid)
                # если блюда нет (удалено/неактивно) — пометим на удаление и пропустим
                if obj is None or getattr(obj, "is_active", True) is False:
                    local_to_delete.append(pid_str)
                    continue
                line_total = (getattr(obj, "price", None) or Decimal("0")) * q
                yield {
                    "product": obj,
                    "qty": q,
                    "line_total": line_total,
                }
            # чистка после итерации
            if local_to_delete or to_delete:
                for k in (*local_to_delete, *to_delete):
                    self.cart.pop(k, None)
                self.save()

        return _gen()
        # def items_detailed(self):
        #     """
        #     Возвращает итератор по позициям корзины с обогащением объектами Product.
    #     Без изменения словаря во время итерации.
    #     """
    #     # делаем снимок текущего словаря, чтобы не словить RuntimeError
    #     snapshot_items = list(self.cart.items())  # [(pid_str, qty), ...]
    
    #     # заранее подтягиваем продукты одним запросом
    #     pids = [int(pid_str) for pid_str, _ in snapshot_items]
    #     products = Product.objects.in_bulk(pids)  # {pid:int -> Product}
    
    #     to_delete = []
    
    #     for pid_str, qty in snapshot_items:
    #         try:
    #             qty = int(qty)
    #         except (TypeError, ValueError):
    #             to_delete.append(pid_str)
    #             continue
    #         if qty <= 0:
    #             to_delete.append(pid_str)
    #             continue

    #         pid = int(pid_str)
    #         obj = products.get(pid)
    #         if not obj:
    #             # блюдо удалено/неактивно — отметим на удаление после цикла
    #             to_delete.append(pid_str)
    #             continue

    #     line_total = (obj.price or Decimal("0")) * qty
    #     yield {
    #         "product": obj,
    #         "qty": qty,
    #         "line_total": line_total,
    #     }

    #     # чистим корзину уже после обхода
    #     if to_delete:
    #         for k in to_delete:
    #             self.cart.pop(k, None)
    #         self.save()

    #     def total(self):
    #         return sum(i["line_total"] for i in self.items_detailed())


