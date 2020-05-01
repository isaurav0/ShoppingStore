from django.contrib import admin

from django.contrib import admin
from products.models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCart)
admin.site.register(ProductComment)
admin.site.register(ProductCommentReply)
