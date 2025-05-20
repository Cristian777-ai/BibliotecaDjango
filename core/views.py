from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Libro
from .forms import LibroForm

class BorrowerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'usuario_regular'

class LibroCreateView(CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'core/libro_form.html'
    success_url = reverse_lazy('core:libro_list')

class LibroUpdateView(UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'core/libro_form.html'
    success_url = reverse_lazy('core:libro_list')

class LibroDeleteView(DeleteView):
    model = Libro
    template_name = 'core/libro_confirm_delete.html'
    success_url = reverse_lazy('core:libro_list')

class LibroListView(LoginRequiredMixin, ListView):
    model = Libro
    template_name = 'core/libro_list.html'
    context_object_name = 'libros'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(author__icontains=q)
            )
        return qs

class LibroDetailView(DetailView):
    model = Libro
    template_name = 'core/libro_detail.html'
    context_object_name = 'libro'

class LibroBorrowView(LoginRequiredMixin, BorrowerRequiredMixin, View):
    def get(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        if libro.stock < 1:
            messages.error(request, 'No hay unidades disponibles para préstamo.')
        else:
            request.user.borrowed_books.add(libro)
            libro.stock -= 1
            libro.save()
            messages.success(request, f'Has prestado “{libro.title}”.')
        return redirect('core:libro_detail', pk=pk)

class LibroReturnView(LoginRequiredMixin, BorrowerRequiredMixin, View):
    def get(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        if libro not in request.user.borrowed_books.all():
            messages.error(request, 'No has prestado este libro.')
        else:
            request.user.borrowed_books.remove(libro)
            libro.stock += 1
            libro.save()
            messages.success(request, f'Has devuelto “{libro.title}”.')
        return redirect('core:libro_detail', pk=pk)
    
class MisBorrowedListView(LoginRequiredMixin, ListView):
    model = Libro
    template_name = 'core/mis_prestados.html'
    context_object_name = 'libros'
    
    def get_queryset(self):
        # Devuelve solo los libros que el usuario ha prestado
        return self.request.user.borrowed_books.all()