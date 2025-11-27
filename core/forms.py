from django import forms
from .models import Category, Product


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


