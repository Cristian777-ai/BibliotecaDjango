from django import forms
from .models import Libro

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['title', 'author', 'publication_year', 'stock', 'cover']