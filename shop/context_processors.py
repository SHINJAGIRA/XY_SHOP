from .models import *

def user_data(request):
    user=request.user
    products_in_stock=ProductIn.objects.select_related('product_id').all()
    product=Product.objects.all()
    products_without_stock=Product.objects.exclude(
        id__in=ProductIn.objects.values_list("product_id",flat=True)
    )
    
    products_sold=ProductOut.objects.all()
    context={}
    if user.is_authenticated:
        context={
            'username':user.username,
            'email':user.email,
            'products':products_in_stock,
            'sold':products_sold,
            'product_names':product,
            'out_stock':products_without_stock
            
        }
    return context