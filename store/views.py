#from multiprocessing import context
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import ReviewForm
#envia los mensajes de ecito y alerta
from django.contrib import messages
#validar usuario para enviar comentarios
from orders.models import OrderProduct

# Create your views here, funcion de todos los productos por categoria
def store(request, category_slug=None): # trae todos los productos, pero si existe categoria, entonces extrae todo los productos que sean de la categoria.

    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')
        paginator = Paginator(products, 5) #muestrame solo 5 productos en la pagina en grupos de 5 por pagina
        page = request.GET.get('page') #traeme la pagina que esta en el browser actulmente ahora se a que pagina quiere entrar el cliente, ya que como son de grupos puedes estar en la 1, 2, 3, 4, 5 depende en el grupo de 5 que este el producto. tre el dato de la pagina numero
        paged_products = paginator.get_page(page) #ahora paginator tiene los productos y los vamos a mandar a treaer
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 5) #muestrame solo 5 productos en la pagina en grupos de 5
        page = request.GET.get('page') #traeme la pagina que esta en el browser actulmente ahora se a que pagina quiere entrar el cliente.
        paged_products = paginator.get_page(page) #ahora paginator tiene los productos y los vamos a mandar a treaer los productos por pagina en la que se encunetre por eso hacemos la instancia de paginator.get_page.
        product_count = products.count()
        
    context = {
        'products': paged_products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)

#=========================================================pagina productos y detalles funcion=============
def product_detail(request, category_slug, product_slug):

    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
   


    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
   

    context = {
        'single_product': single_product,
        'in_cart':in_cart,
        'orderproduct':orderproduct,
        'reviews': reviews,
    }

    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword) )
            products_count = products.count()
    
    context = {
        'products': products,
        'products_count': products_count
    }
    
    return render(request, 'store/store.html', context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            if form.is_valid():
                data = form.save(commit=False)
                data.ip = request.META.get('REMOTE_ADDR')
                data.save()
                messages.success(request, '¡Muchas gracias! Tu comentario ha sido actualizado.')
            else:
                messages.error(request, 'Por favor, selecciona un rating.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, '¡Muchas gracias! Tu comentario fue enviado con éxito.')
                return redirect(url)
            else:
                messages.error(request, 'Por favor, selecciona un rating.')
                return redirect(url)




