# filters.py
import django_filters
from django import forms
from .models import Product

class ProductFilter(django_filters.FilterSet):
    # 1. To jest kluczowe - musimy zdefiniować pole 'title'
    title = django_filters.CharFilter(
        field_name='title',      # Nazwa pola w modelu
        lookup_expr='icontains', # icontains = ignoruj wielkość liter, szukaj fragmentu
        label='Szukaj kota'      # Etykieta
    )

    # 2. Twoje sortowanie
    ordering = django_filters.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('last_update', 'date'),
        ),
        field_labels={
            'price': 'Cena',
            'date': 'Data',
        },
        label='Sortuj według'
    )

    class Meta:
        model = Product
        # Tutaj wpisujemy tylko pola, które NIE są zdefiniowane wyżej ręcznie
        fields = ['category']