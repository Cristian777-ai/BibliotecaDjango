from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from .models import Libro, Usuario

class LibroModelTest(TestCase):
    def setUp(self):
        self.libro = Libro.objects.create(
            title="Test Libro",
            author="Autor Test",
            publication_year=2020,
            stock=5
        )

    def test_str_representation(self):
        self.assertEqual(
            str(self.libro),
            "Test Libro by Autor Test (2020)"
        )

    def test_initial_stock(self):
        self.assertEqual(self.libro.stock, 5)

class WebViewPermissionsTest(TestCase):
    def setUp(self):
        # Usuarios de prueba
        self.admin = Usuario.objects.create_user(
            username='admin', password='adminpass', role='administrador'
        )
        self.regular = Usuario.objects.create_user(
            username='regular', password='regularpass', role='usuario_regular'
        )
        self.libro = Libro.objects.create(
            title="Libro1", author="A.", publication_year=2000, stock=1
        )
        self.client = Client()

    def test_login_required_redirect(self):
        resp = self.client.get(reverse('core:libro_list'))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse('login'), resp.url)

    def test_admin_can_access_create(self):
        self.client.login(username='admin', password='adminpass')
        resp = self.client.get(reverse('core:libro_create'))
        self.assertEqual(resp.status_code, 200)

    def test_regular_cannot_access_create(self):
        self.client.login(username='regular', password='regularpass')
        resp = self.client.get(reverse('core:libro_create'))
        self.assertEqual(resp.status_code, 403)

class ApiTestCase(TestCase):
    def setUp(self):
        self.admin = Usuario.objects.create_user(
            username='apiadmin', password='apipass', role='administrador'
        )
        self.regular = Usuario.objects.create_user(
            username='apiregular', password='apipass', role='usuario_regular'
        )
        self.libro = Libro.objects.create(
            title="API Libro", author="API A.", publication_year=2010, stock=2
        )
        self.client = APIClient()

    def test_list_books(self):
        self.client.login(username='apiregular', password='apipass')
        resp = self.client.get('/api/libros/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp.json(), list)

    def test_create_book_admin(self):
        self.client.login(username='apiadmin', password='apipass')
        data = {"title": "Nuevo API", "author": "X", "publication_year": 2021, "stock": 3}
        resp = self.client.post('/api/libros/', data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_create_book_regular_forbidden(self):
        self.client.login(username='apiregular', password='apipass')
        data = {"title": "Fail API", "author": "X", "publication_year": 2021, "stock": 1}
        resp = self.client.post('/api/libros/', data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_borrow_and_return(self):
        self.client.login(username='apiregular', password='apipass')
        # Préstamo
        resp = self.client.post(f'/api/libros/{self.libro.pk}/prestamo/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.libro.refresh_from_db()
        self.assertEqual(self.libro.stock, 1)
        # Devolución
        resp = self.client.post(f'/api/libros/{self.libro.pk}/devolucion/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.libro.refresh_from_db()
        self.assertEqual(self.libro.stock, 2)

    def test_borrow_out_of_stock(self):
        self.libro.stock = 0
        self.libro.save()
        self.client.login(username='apiregular', password='apipass')
        resp = self.client.post(f'/api/libros/{self.libro.pk}/prestamo/')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_without_borrow(self):
        self.client.login(username='apiregular', password='apipass')
        resp = self.client.post(f'/api/libros/{self.libro.pk}/devolucion/')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
