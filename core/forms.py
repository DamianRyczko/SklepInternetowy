from django import forms
from .models import Category, Product, Address


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        # We specify which fields to include in the form
        fields = ['title', 'description']

        # Optional: Add CSS classes for styling (e.g., if using Bootstrap)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'inventory', 'category', 'image']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
                   'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
                   'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter product price'}),
                   'inventory': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter product inventory'}),
                   'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select category'}),
                   'image': forms.FileInput(attrs={'class': 'form-control'}),
                   }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_address', 'city', 'zip_code']

        widgets = {
            'street_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter street name'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter zipcode'}),
        }

class CardForm(forms.Form):

    card_number = forms.CharField(label = 'Numer Karty',
                                  max_length= 16,
                                  min_length= 16,
                                  widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '0000 0000 0000 0000'}))

    card_owner = forms.CharField(label = 'Właściciel',
                                 widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Imie Nazwisko'}))

    expiry_date = forms.CharField(label = 'Data ważności',
                                  max_length= 5,
                                  widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'MM/YY'}))

    cvv = forms.CharField(label = 'CVV',
                          max_length= 3,
                          widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '123'}))

class BlikForm(forms.Form):

    blik_code = forms.CharField(label = 'Kod BLIK',
                                  max_length= 6,
                                  min_length= 6,
                                  widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '000 000'}))
