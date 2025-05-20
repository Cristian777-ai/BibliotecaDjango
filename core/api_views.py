from rest_framework import viewsets
from .models import Libro
from .serializers import LibroSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsRegularUser

class LibroViewSet(viewsets.ModelViewSet):
    """
    CRUD de libros, usando permisos IsAdminOrReadOnly:
    -- GET, HEAD, OPTIONS abiertos
    -- POST/PUT/PATCH/DELETE solo para administradores
    """
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(
    detail=True,
    methods=['post'],
    permission_classes=[IsRegularUser],
    url_path='prestamo'
    )
    def prestar(self, request, pk=None):
     libro = self.get_object()
     if libro.stock < 1:
        return Response({'detail': 'Sin unidades disponibles.'}, status=status.HTTP_400_BAD_REQUEST)
     request.user.borrowed_books.add(libro)
     libro.stock -= 1
     libro.save()
     serializer = self.get_serializer(libro)
     return Response(serializer.data)

    @action(
    detail=True,
    methods=['post'],
    permission_classes=[IsRegularUser],
    url_path='devolucion'
    )
    def devolver(self, request, pk=None):
     libro = self.get_object()
     if libro not in request.user.borrowed_books.all():
        return Response({'detail': 'No has prestado este libro.'}, status=status.HTTP_400_BAD_REQUEST)
     request.user.borrowed_books.remove(libro)
     libro.stock += 1
     libro.save()
     serializer = self.get_serializer(libro)
     return Response(serializer.data)

