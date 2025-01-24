from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect 
from .models import Product, Category
from .forms import ProductForm, SearchForm 
from django.core.paginator import Paginator 

def product_detail_api(request, pk):
    product = get_object_or_404(Product, pk=pk)
    data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": float(product.price),
        "category": product.category.name,
    }
    return JsonResponse(data)

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

from django.db.models import Avg
def product_list(request):
    # フォームの初期化
    form = SearchForm(request.GET or None)
    
    # 商品の初期クエリセット
    products = Product.objects.all()

    # 検索フォームの処理
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            products = products.filter(name__icontains=query)  # 商品名で検索

    # カテゴリフィルタリング
    category_name = request.GET.get('category')
    if category_name:
        try:
            category = Category.objects.get(name=category_name)
            products = products.filter(category_id=category.id)
        except Category.DoesNotExist:
            products = products.none()

    # 価格フィルタリング（最低価格・最高価格）
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # 並び替え処理
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # 商品ごとに評価を計算
    for product in products:
        reviews = Review.objects.filter(product=product)
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        product.full_stars = list(range(1, int(average_rating) + 1))
        product.empty_stars = list(range(int(average_rating) + 1, 6))
        product.average_rating = average_rating

    # 評価が高い順に商品を並べ替え（上位5つ）
    recommended_products = sorted(products, key=lambda p: p.average_rating, reverse=True)[:5]

    # ページネーション設定
    paginator = Paginator(products, 10)  # 1ページに10件表示
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # テンプレートに渡すデータ
    return render(request, 'product_list.html', {
        'form': form,  # 検索フォーム
        'page_obj': page_obj,  # ページネーションされた商品一覧
        'recommended_products': recommended_products  # おすすめ商品
    })

# ほしい物リスト（仮）
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Wishlist

@login_required
def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        # アイテムがリストに追加された
        return redirect('wishlist')  # ほしい物リストページにリダイレクト
    else:
        # すでにリストにある場合は何もしない
        return redirect('wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    wishlist_item = Wishlist.objects.get(user=request.user, product=product)
    wishlist_item.delete()  # リストから削除
    return redirect('wishlist')  # ほしい物リストページにリダイレクト

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product  # モデルをインポート
from .models import Review  # レビュー用モデルもインポート
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .models import Product, Review
from .forms import ReviewForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, Review

def product_detail_api(request, pk):
    product = get_object_or_404(Product, pk=pk)
    data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category.name,
        "is_authenticated": request.user.is_authenticated,  # ここを追加
    }
    return JsonResponse(data)

def product_reviews_api(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all()
    reviews_data = [
        {
            "user": review.user.username,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at.strftime("%Y-%m-%d %H:%M"),
        }
        for review in reviews
    ]
    return JsonResponse(reviews_data, safe=False)

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Productを取得
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product  # Productを設定
            review.user = request.user  # 現在のユーザーを設定
            review.save()
            return redirect(reverse('product_list'))
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'product': product, 'range': range(1, 6)})

# 以下決済画面・購入機能
from django.shortcuts import redirect, get_object_or_404
from .models import Product, Cart

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')  # カートページへリダイレクト


from django.shortcuts import render
from .models import Cart

def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

from .models import Order

def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)  # 合計金額を計算

    if request.method == "POST":
        # カートの商品を注文として保存
        for item in cart_items:
            Order.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                total_price=item.product.price * item.quantity,
                status='completed',
            )
        cart_items.delete()  # カートを空にする
        return render(request, 'checkout_success.html')  # 成功画面へ

    # 合計金額をテンプレートに渡す
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})



def remove_from_cart(request, product_id):
    if request.method == "POST":
        # カートアイテムを取得して削除
        cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
        cart_item.delete()
    return redirect('cart_view')  # カートページにリダイレクト

