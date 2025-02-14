from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    publication_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'books'

