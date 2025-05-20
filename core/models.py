from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLE_CHOICES = [
        ('usuario_regular', 'Usuario Regular'),
        ('administrador', 'Administrador'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='usuario_regular')
    borrowed_books = models.ManyToManyField('Libro', blank=True, related_name='borrowers')

class Libro(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_year = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    cover = models.ImageField(
        upload_to='covers/',
        blank=True,
        null=True,
        help_text='Portada del libro'
    )

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"