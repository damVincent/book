from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Author(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='author_images/', blank=True)
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)
    biography = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class BestSellingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-sales_count')

class Book(models.Model):
    title = models.CharField(max_length=200)
    quote = models.CharField(max_length=250, blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='books')
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cover_image = models.ImageField(upload_to='book_covers/')
    description = models.TextField()
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    sales_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    copyright = models.TextField(blank=True, null=True)
    dedication = models.TextField(blank=True, null=True)
    foreword = models.TextField(blank=True, null=True)
    prologue = models.TextField(blank=True, null=True)
    epilogue = models.TextField(blank=True, null=True)
    epigraph = models.TextField(blank=True, null=True)
    copies_released = models.PositiveIntegerField(default=0)
    happy_readers = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['genre']),
            models.Index(fields=['publication_date']),
        ]

    objects = models.Manager()
    best_selling_objects = BestSellingManager()

    def record_sale(self):
        self.sales_count += 1
        self.save()

    class Meta:
        ordering = ['-sales_count']

    def __str__(self):
        return self.title

    @classmethod
    def best_selling(cls):
        return cls.best_selling_objects.all()
    
    def get_cover_image_url(self):
        if self.cover_image:
            return self.cover_image.url
        return None


class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='review_images/', blank=True)
    email = models.EmailField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.book.title} by {self.name}"

class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"messgae from {self.name}"