from django.urls import path
from .views import (
    LibroListView, LibroDetailView,
    LibroCreateView, LibroUpdateView, LibroDeleteView,
    LibroBorrowView, LibroReturnView,
    MisBorrowedListView,
)

app_name = 'core'

urlpatterns = [
    path('libros/', LibroListView.as_view(), name='libro_list'),
    path('libros/<int:pk>/', LibroDetailView.as_view(), name='libro_detail'),
    path('libros/nuevo/', LibroCreateView.as_view(), name='libro_create'),
    path('libros/<int:pk>/editar/', LibroUpdateView.as_view(), name='libro_update'),
    path('libros/<int:pk>/borrar/', LibroDeleteView.as_view(), name='libro_delete'),
    path('libros/<int:pk>/prestamo/', LibroBorrowView.as_view(), name='libro_borrow'),
    path('libros/<int:pk>/devolucion/', LibroReturnView.as_view(), name='libro_return'),
    path('mis-prestados/', MisBorrowedListView.as_view(), name='mis_prestados'),
]