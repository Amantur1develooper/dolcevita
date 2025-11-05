from django import forms
from django.utils.translation import gettext_lazy as _

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
            "placeholder": _("Пожелания: у окна, без лука, день рождения..."),
            "class":"w-full border rounded-xl px-3 py-2"
        })
    )
