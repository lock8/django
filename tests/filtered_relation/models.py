from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Author(models.Model):
    name = models.CharField(max_length=50, unique=True)
    favourite_books = models.ManyToManyField(
        'Book',
        related_name='preferred_by_authors',
        related_query_name='preferred_by_authors')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


@python_2_unicode_compatible
class Editor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


@python_2_unicode_compatible
class Book(models.Model):
    AVAILABLE = 'available'
    RESERVED = 'reserved'
    RENTED = 'rented'
    STATES = [
        (AVAILABLE, 'Available'),
        (RESERVED, 'reserved'),
        (RENTED, 'Rented'),
    ]
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author,
                               related_name='books',
                               related_query_name='book',
                               on_delete=models.CASCADE)
    editor = models.ForeignKey(Editor, on_delete=models.CASCADE)
    state = models.CharField(max_length=9, choices=STATES, default=AVAILABLE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']


@python_2_unicode_compatible
class Borrower(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


@python_2_unicode_compatible
class Reservation(models.Model):
    NEW = 'new'
    STOPPED = 'stopped'
    STATES = [(NEW, 'New'),
              (STOPPED, 'Stopped')]
    borrower = models.ForeignKey(Borrower,
                                 related_name='reservations',
                                 related_query_name='reservation',
                                 on_delete=models.CASCADE)
    book = models.ForeignKey(Book,
                             related_name='reservations',
                             related_query_name='reservation',
                             on_delete=models.CASCADE)
    state = models.CharField(max_length=7, choices=STATES, default=NEW)

    def __str__(self):
        return '-'.join(self.book.name, self.borrower.name, self.state)

    class Meta:
        ordering = ['id']


@python_2_unicode_compatible
class RentalSession(models.Model):
    NEW = 'new'
    STOPPED = 'stopped'
    STATES = [(NEW, 'New'),
              (STOPPED, 'Stopped')]
    borrower = models.ForeignKey(Borrower,
                                 related_name='rental_sessions',
                                 related_query_name='rental_session',
                                 on_delete=models.CASCADE)
    book = models.ForeignKey(Book,
                             related_name='rental_sessions',
                             related_query_name='rental_session',
                             on_delete=models.CASCADE)
    state = models.CharField(max_length=7, choices=STATES, default=NEW)

    def __str__(self):
        return '-'.join(self.book.name, self.borrower.name, self.state)

    class Meta:
        ordering = ['id']
