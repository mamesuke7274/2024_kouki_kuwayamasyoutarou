from django.shortcuts import render, get_object_or_404, redirect 
from .models import Product, Category 
from .forms import ProductForm, SearchForm 
from django.core.paginator import Paginator 
 
def product_create(request): 
    if request.method == 'POST': 
        form = ProductForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect('product_list') 
    else: 
        form = ProductForm() 
    return render(request, 'product_form.html', {'form': form}) 
 
def product_detail(request, pk): 
    product = get_object_or_404(Product, pk=pk) 
    return render(request, 'product_detail.html', {'product': product}) 
 
def product_update(request, pk): 
    product = get_object_or_404(Product, pk=pk) 
    if request.method == 'POST': 
        form = ProductForm(request.POST, instance=product) 
        if form.is_valid(): 
            form.save() 
            return redirect('product_detail', pk=product.pk) 
    else: 
        form = ProductForm(instance=product) 
   # product オブジェクトをテンプレートに渡す 
    return  render(request,  'product_form.html',  {'form':  form,  'product': product})

