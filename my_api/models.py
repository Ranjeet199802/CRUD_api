from django.db import models


# Create your models here.
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    book_name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.book_name
