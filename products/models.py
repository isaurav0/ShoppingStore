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

STATE_CHOICES = (
    ('Active', 'Active'),
    ('Completed', 'Completed'),
    ('Frozen', 'Frozen')
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


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=16)
    fullname = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    order_detail = models.TextField(default='')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, choices=STATE_CHOICES, default='Active')

    def __str__(self):
        return f'From {self.user} at '\
               f'{self.order_date.strftime("%b %-d, %Y, %-I:%-M %p")}'


class ProductCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, on_delete=models.DO_NOTHING,
        blank=True, null=True, default=None
    )
    quantity = models.IntegerField(default=1)


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return json.dumps({"comment_id": "%d" % self.id, "comment_text": "%s" %
                          self.comment, "created_at": self.created_at.strftime(
                            "%b %-d, %Y, %-I:%-M %p").lower()})


class ProductCommentReply(models.Model):
    comment = models.ForeignKey(ProductComment, on_delete=models.CASCADE,
                                blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.CharField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return json.dumps({"reply_text": self.reply, "created_at":
                          self.created_at.strftime("%b %-d, %Y, %-I:%-M %p").
                          lower()})
