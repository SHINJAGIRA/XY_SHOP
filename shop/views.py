

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *  
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator 
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
import os
from datetime import datetime

# Create your views here.
def login_view(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request,'invalid username or password')
    
    return render(request,'login.html')

def signup_view(request):
    if request.method=='POST':
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user = User.objects.create_user(
                first_name=firstname,
                last_name=lastname,
                email=email,
                username=username,
                password=password
        )
        user.save()
        return redirect('login')
    else:
        return render(request,'signup.html')


@login_required
def dashboard(request):
    return render(request,'dashboard.html')
@login_required
def stock_out(request):
    return render(request,'stock_out.html')
@login_required
def stock(request):
    if request.method=='POST':
        print(request.POST)
        product_id = int(request.POST.get('product_id'))
        action=request.POST.get('action')
        quantity = int(request.POST.get('quantity'))
        # Fetch the product to update based on pk
        product = get_object_or_404(ProductIn, id=product_id)
        if action =='remove':
            product.quantity -= quantity
        else:
            product.quantity += quantity
        product.save()

        return redirect('stock') 
    return render(request,'stock.html')

def logout_view(request):    
    logout(request)
    return redirect('accounts/login')


def render_to_pdf(template_src, context_data={}):
    html_string = render_to_string(template_src, context_data)
    response = HttpResponse(content_type="application/pdf")
    file_name=f'report on {datetime.now().strftime("%Y-%m-%d")}.pdf'
    response["Content-Disposition"] = f'attachment; filename="{file_name}"'

    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_path = os.path.join(temp_dir, "temp_report.pdf")
        HTML(string=html_string).write_pdf(pdf_path)

        # Read and write to response
        with open(pdf_path, 'rb') as f:
            response.write(f.read())

    return response
@login_required
def report_pdf(request):
    products_in_stock=ProductIn.objects.select_related('product_id').all()
    products_sold=ProductOut.objects.all()
    context_data={
        'stock':products_in_stock,
        'sold':products_sold
    }
    return render_to_pdf('report.html',context_data)


def add_product_in_stock(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        unit_price = request.POST.get('unit_price')
        date = request.POST.get('added_at')

        # Fetch the Product instance
        product = get_object_or_404(Product, id=int(product_id))

        product_in = ProductIn(
            product_id=product,  
            quantity=int(quantity),
            unit_price=int(unit_price),
            added_at=date,
        )
        product_in.save()

        return redirect('stock')

def sell_product(request):
    product=Product.objects.all()
    if request.method=='POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        unit_price = request.POST.get('unit_price')
        date = request.POST.get('added_at')

        # Fetch the Product instance
        product = get_object_or_404(Product, id=int(product_id))

        product_out = ProductOut(
            product_id=product,  
            quantity=int(quantity),
            unit_price=int(unit_price),
            added_at=date,
        )
        product_out.save()
        return redirect('stock_out')


def add_product(request):
    if request.method=="POST":
        product_name=request.POST.get('product_name')

        product=Product(product_name=product_name)
        product.save()
        return redirect('dashboard')
    return render(request,'addproduct.html')

def delete_product(request,pk):
    item = get_object_or_404(ProductIn, pk=pk)
    if request.method == "POST":
        item.delete()
        return redirect('stock')
    return render(request, 'delete_confirmation.html', {'item': item})
