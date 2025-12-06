from django import forms
from django.utils.translation import gettext_lazy as _


# core/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _

FLOOR_CHOICES = [
    ("1", _("1 этаж Dolce Bakery& karaoke")),
    ("2", _("2 этаж Dolce Family")),
    ("3", _("3 этаж restaurant MONE")),  # при желании можно подписать как "3 этаж (Mone)"
]
# core/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _

INPUT_CLS = (
    "w-full border border-stone-300 rounded-xl px-3 py-2 "
    "focus:outline-none focus:ring-2 focus:ring-emerald-500/40 "
    "focus:border-emerald-500 placeholder-stone-400"
)

class ReservationForm(forms.Form):
    name = forms.CharField(
        label=_("Имя"),
        max_length=80,
        widget=forms.TextInput(attrs={"placeholder": _("Ваше имя"), "class":"w-full border rounded-xl px-3 py-2"})
    )
    phone = forms.CharField(
        label=_("Телефон"),
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": _("Ваш телефон"), "class":"w-full border rounded-xl px-3 py-2"})
    )
    date = forms.DateField(
        label=_("Дата"),
        widget=forms.DateInput(attrs={"type":"date", "class":"w-full border rounded-xl px-3 py-2"})
    )
    time = forms.TimeField(
        label=_("Время"),
        widget=forms.TimeInput(attrs={"type":"time", "class":"w-full border rounded-xl px-3 py-2"})
    )
    guests = forms.IntegerField(
        label=_("Гостей"),
        min_value=1, max_value=20,
        widget=forms.NumberInput(attrs={"placeholder":"2", "class":"w-full border rounded-xl px-3 py-2"})
    )
    comment = forms.CharField(
        label=_("Комментарий"),
        required=False,
        widget=forms.Textarea(attrs={
            "rows":3,
            "placeholder": _("Пожелания: у окна, на террасе, день рождения..."),
            "class":"w-full border rounded-xl px-3 py-2"
        })
    )
    floor = forms.ChoiceField(  # ← стилизованный select
        label=_("Этаж"),
        choices=FLOOR_CHOICES,
        widget=forms.Select(attrs={
            "class": INPUT_CLS,
        })
    )