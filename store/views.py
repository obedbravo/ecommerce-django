from multiprocessing import context
from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here, funcion de todos los productos por categoria
def store(request, category_slug=None): # trae todos los productos, pero si existe categoria, entonces extrae todo los productos que sean de la categoria.

    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 5) #muestrame solo 5 productos en la pagina en grupos de 5 por pagina
        page = request.GET.get('page') #traeme la pagina que esta en el browser actulmente ahora se a que pagina quiere entrar el cliente, ya que como son de grupos puedes estar en la 1, 2, 3, 4, 5 depende en el grupo de 5 que este el producto. tre el dato de la pagina numero
        paged_products = paginator.get_page(page) #ahora paginator tiene los productos y los vamos a mandar a treaer
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
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
    
    context = {
        'single_product': single_product,
        'in_cart':in_cart,
    }

    return render(request, 'store/product_detail.html', context)