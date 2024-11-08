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
def product_delete(request, pk): 
    product = get_object_or_404(Product, pk=pk) 
    if request.method == 'POST': 
        product.delete() 
        return redirect('product_list') 
    return render(request, 'product_confirm_delete.html', {'product': product}) 
 
def product_list(request): 
    products = Product.objects.all() 
    return render(request, 'product_list.html', {'products': products}) 
 
def search_view(request): 
    form = SearchForm(request.GET or None) 
    results = Product.objects.all()  # クエリセットの初期化 
    if form.is_valid(): 
        query = form.cleaned_data['query'] 
        if query: 
            results = results.filter(name__icontains=query) 
    # カテゴリフィルタリング 
    category_name = request.GET.get('category') 
    if category_name: 
        try: 
            # カテゴリ名に基づいてカテゴリIDを取得 
            category = Category.objects.get(name=category_name) 
            results = results.filter(category_id=category.id) 
        except Category.DoesNotExist: 
            results = results.none() # 存在しないカテゴリの場合、結果を空にする 
            category = None 
    # 価格のフィルタリング（最低価格・最高価格） 
    min_price = request.GET.get('min_price') 
    max_price = request.GET.get('max_price') 