from django.db import models
from django.contrib.auth.models import User

class Category(models.Model): 
    name = models.CharField(max_length=255) 

    def __str__(self): 
        return self.name 

class Product(models.Model): 
    id = models.BigAutoField(primary_key=True) 
    name = models.CharField(max_length=255) 
    thumbnail = models.ImageField(upload_to='product_images/',null= True,blank=True)
    description = models.TextField() 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)  # 1はカテゴリID 

    def __str__(self): 
        return self.name

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlists")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # 同じ商品は1回だけ追加可能

    def __str__(self):
        return f"{self.user.username}'s Wishlist - {self.product.name}"