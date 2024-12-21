from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=ProductOut)
def reduce_stock_on_outgoing(sender, instance, created, **kwargs):
    if created:
        # Retrieve the ProductIn instance associated with this ProductOut
        product = instance.product_id
        product_in=ProductIn.objects.filter(product_id=product).first()
        if product_in.quantity >= instance.quantity:
            # Subtract the quantity of ProductOut from ProductIn
            product_in.quantity -= instance.quantity
            product_in.save()
        else:
            # Handle insufficient stock (optional: raise an error or warning)
            print(f"Warning: Insufficient stock for {product_in.product_id.product_name}")