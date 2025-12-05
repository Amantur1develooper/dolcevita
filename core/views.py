from django.shortcuts import render

# Create your views here.
# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from urllib.parse import quote_plus

from .models import Product, Category
from .cart import Cart

def home(request):
    cats = Category.objects.all().prefetch_related("products")
    return render(request, "core/home.html", {"cats": cats})

def add_to_cart(request, product_id):
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")
    qty = int(request.POST.get("qty", 1))
    get_object_or_404(Product, pk=product_id, is_active=True)
    cart = Cart(request)
    cart.add(product_id, qty)

    # если AJAX — отдать JSON с новым количеством
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": True, "count": len(cart)})

    # fallback (если кто-то отправит обычный POST)
    return redirect("core:cart_detail")
# def add_to_cart(request, product_id):
#     if request.method != "POST":
#         return HttpResponseBadRequest("POST only")
#     qty = int(request.POST.get("qty", 1))
#     get_object_or_404(Product, pk=product_id, is_active=True)
#     cart = Cart(request)
#     cart.add(product_id, qty)
#     # для SPA-ощущения можно вернуть JSON
#     if request.headers.get("x-requested-with") == "XMLHttpRequest":
#         return JsonResponse({"ok": True, "count": len(cart)})
#     return redirect("core:cart_detail")

def update_cart(request, product_id):
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")
    qty = int(request.POST.get("qty", 1))
    get_object_or_404(Product, pk=product_id, is_active=True)
    cart = Cart(request)
    cart.add(product_id, qty, replace=True)
    return redirect("core:cart_detail")

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": True, "count": len(cart)})
    return redirect("core:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    items = list(cart.items_detailed())         # ← один раз собрали
    total = sum(i["line_total"] for i in items) # ← один раз посчитали
    return render(request, "core/cart.html", {
        "cart": cart,               # оставим, если где-то нужен len(cart)
        "cart_items": items,        # ← используем в шаблоне
        "cart_total": total,        # ← используем в шаблоне
    })
# def cart_detail(request):
#     cart = Cart(request)
#     return render(request, "core/cart.html", {"cart": cart})


def checkout_whatsapp(request):
    
    phone = getattr(settings, "WHATSAPP_PHONE", "").replace("+", "")
    if not phone:
        return HttpResponseBadRequest("WHATSAPP_PHONE не задан в settings")

    cart = Cart(request)
    items = list(cart.items_detailed())           # ← один список
    if not items:
        return redirect("core:home")

    total = sum(i["line_total"] for i in items)

    lines = ["Dolcevita — новый заказ:"]
    for it in items:
        p = it["product"]
        lines.append(f"• {p.name} × {it['qty']} = {it['line_total']:.2f} сом")
    lines.append(f"Итого: {total:.2f} сом")

    name  = request.GET.get("name", "").strip()
    table = request.GET.get("table", "").strip()
    note  = request.GET.get("note", "").strip()
    if name:  lines.append(f"Имя: {name}")
    if table: lines.append(f"Стол/доставка: {table}")
    if note:  lines.append(f"Примечание: {note}")

    text = quote_plus("\n".join(lines))
    return HttpResponseRedirect(f"https://wa.me/{phone}?text={text}")
# def checkout_whatsapp(request):
#     """
#     Генерируем текст заказа и редиректим в WhatsApp.
#     Номер берём из settings.WHATSAPP_PHONE = '+39XXXXXXXXXX'
#     """
#     phone = getattr(settings, "WHATSAPP_PHONE", "").replace("+", "")
#     if not phone:
#         return HttpResponseBadRequest("WHATSAPP_PHONE не задан в settings")

#     cart = Cart(request)
#     if len(cart) == 0:
#         return redirect("core:home")

#     lines = ["Dolcevita — новый заказ:"]
#     for item in cart.items_detailed():
#         p = item["product"]
#         lines.append(f"• {p.name} × {item['qty']} = {item['line_total']:.2f}сом")
#     lines.append(f"Итого: {cart.total():.2f}сом")

#     # необязательные поля клиента (можно добавить простую форму на cart.html)
#     name = request.GET.get("name", "").strip()
#     table = request.GET.get("table", "").strip()  # если dine-in
#     note = request.GET.get("note", "").strip()
#     if name:
#         lines.append(f"Имя: {name}")
#     if table:
#         lines.append(f"Стол: {table}")
#     if note:
#         lines.append(f"Примечание: {note}")

#     text = quote_plus("\n".join(lines))
#     url = f"https://wa.me/{phone}?text={text}"

#     # По желанию очищаем корзину после перехода:
#     # cart.clear()
#     return HttpResponseRedirect(url)

# core/views.py

def contacts(request):
    return render(request, "core/contacts.html")

def about(request):
    return render(request, "core/about.html")

from urllib.parse import quote_plus
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext as _
from .forms import ReservationForm
# core/views.py
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext as _
from urllib.parse import quote_plus
from .forms import ReservationForm

def reserve(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data

            # Получим человекочитаемую метку этажа из choices
            floor_label = dict(form.fields["floor"].choices).get(d["floor"], d["floor"])

            text = _(
                "Здравствуйте! Хочу забронировать стол.\n"
                "Имя: {name}\n"
                "Телефон: {phone}\n"
                "Дата: {date}\n"
                "Время: {time}\n"
                "Гостей: {guests}\n"
                "Этаж: {floor}\n"
                "Комментарий: {comment}"
            ).format(
                name=d["name"],
                phone=d["phone"],
                date=d["date"].strftime("%Y-%m-%d"),
                time=d["time"].strftime("%H:%M"),
                guests=d["guests"],
                floor=floor_label,
                comment=d.get("comment") or "-"
            )

            number = getattr(settings, "WHATSAPP_PHONE", "")
            if not number:
                
                return render(request, "core/reserve.html", {
                    "form": form,
                    "no_whatsapp": True
                })

            url = f"https://wa.me/{number}?text={quote_plus(text)}"
            return HttpResponseRedirect(url)
    else:
        form = ReservationForm()

    return render(request, "core/reserve.html", {"form": form})


import os
import re
from glob import glob

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static
from django.shortcuts import render

# Небольшой helper: ищем файлы либо в STATIC_ROOT (prod),
# либо в первом STATICFILES_DIRS (dev)
def _find_static_dir():
    if getattr(settings, "STATIC_ROOT", None) and os.path.isdir(settings.STATIC_ROOT):
        return settings.STATIC_ROOT
    dirs = getattr(settings, "STATICFILES_DIRS", [])
    return dirs[0] if dirs else None

def _natural_key(path):
    # .../page-12.webp -> 12 (для естественной сортировки)
    m = re.search(r"page-(\d+)\.webp$", os.path.basename(path))
    return int(m.group(1)) if m else 0

def menu_view(request):
    # URL для PDF (просто через {% static %})
    pdf_url = static("menu/menu-web.pdf")

    # Ищем webp-страницы на диске, строим к ним STATIC-URL’ы
    webp_urls = []
    base_dir = _find_static_dir()
    if base_dir:
        filesystem_glob = os.path.join(base_dir, "menu", "page-*.webp")
        files = sorted(glob(filesystem_glob), key=_natural_key)
        for f in files:
            rel = os.path.relpath(f, base_dir).replace("\\", "/")  # menu/page-1.webp
            try:
                # корректно построить URL независимо от STATIC_URL
                url = staticfiles_storage.url(rel)
            except Exception:
                # fallback (обычно не понадобится)
                url = static(rel)
            webp_urls.append(url)

    ctx = {
        "pdf_url": pdf_url,
        "webp_pages": webp_urls,  # пустой список — тоже ок
    }
    return render(request, "core/menu.html", ctx)
