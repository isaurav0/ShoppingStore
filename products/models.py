from django.contrib.auth.models import AbstractUser
from django.db import models
import json


TYPE_CHOICES = (
    ('THC', 'THC'),
    ('CBD', 'CBD')
)

CATEGORY_CHOICES = (
    ('Sour', 'Sour'),
    ('Spicy', 'Spicy')
)


class User(AbstractUser):
    description = models.CharField(max_length=100, blank=False, default='')


class Product(models.Model):
    title = models.CharField(max_length=100, blank=False)
    image_url = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=False)
    concentration = models.CharField(max_length=200, blank=True)
    product_category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, blank=True)
    product_type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, blank=True)
    product_ingredients = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.title


class ProductCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return json.dumps({'comment_id': self.id, 'comment_text': self.comment}
                          )


class ProductCommentReply(models.Model):
    comment = models.ForeignKey(ProductComment, on_delete=models.CASCADE,
                                blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.CharField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.comment.comment
