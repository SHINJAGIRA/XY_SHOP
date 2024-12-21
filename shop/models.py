from django.db import models

# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product_name
    
class ProductIn(models.Model):
    product_id=models.OneToOneField("Product", on_delete=models.CASCADE)
    added_at=models.DateField(auto_now=False, auto_now_add=False)
    quantity=models.PositiveIntegerField()
    unit_price=models.DecimalField(max_digits=255,decimal_places=2)
    total_price=models.DecimalField(max_digits=255,decimal_places=2,blank=True,null=True)
    def save(self,*args,**kwargs):
        self.total_price=self.unit_price * self.quantity
        super().save(*args,**kwargs)


    def __str__(self):
        return self.product_id.product_name

class ProductOut(models.Model):
    product_id=models.OneToOneField("Product", on_delete=models.CASCADE)
    added_at=models.DateField( auto_now=False, auto_now_add=False)
    quantity=models.PositiveIntegerField()
    unit_price=models.DecimalField( max_digits=15, decimal_places=2)
    total_price=models.DecimalField(max_digits=255,decimal_places=2,blank=True,null=True)
    def __str__(self):
        return self.product_id.product_name
    def save(self, *args, **kwargs):
        # Calculate the total price
        self.total_price = self.unit_price * self.quantity

        # Fetch the related ProductIn instance
        try:
            product_in = ProductIn.objects.get(product_id=self.product_id)
        except ProductIn.DoesNotExist:
            raise ValidationError(f"No stock available for product: {self.product_id}")

        # Check if there's enough stock
        if product_in.quantity < self.quantity:
            raise ValidationError(f"Insufficient stock for product: {self.product_id}")

        # Deduct the quantity from ProductIn
        product_in.quantity -= self.quantity
        product_in.save()

        # Save the ProductOut instance
        super().save(*args, **kwargs)