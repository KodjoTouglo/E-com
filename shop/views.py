import json
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Product, Size, Images, Variants, Slide, Categoryproduct

def base(request, category_slug=None):
    imgcatgry = Categoryproduct.objects
    image = Slide.objects
    featured_product = Product.objects.all().order_by('id')[:6]
    latest_product = Product.objects.all().order_by('-id')[:4]
    context = {
        'imgcatgry': imgcatgry,
        'image': image,
        'featured_product': featured_product,
        'latest_product': latest_product
    }
    return render(request, 'shop/base.html', context)




def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    query = request.GET.get('q')
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    images = Images.objects.filter(product_id=id)
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
    }

    if product.variant != "None":
        if request.method == 'POST':
            variant_id = request.POST.get('variantid')
            variant = Variants.object.get(id=variant_id)
            sizes = Variants.objects.raw('SELECT * FROM shop_variants WHERE product_id=%s GROUP BY size_id',[id])
            colors = Variants.objects.filter(product_id=id,size_id=variant.size_id)
            query += variant.name+ ' Size:' +str(variant.size) +' Color:' +str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            sizes = Variants.objects.raw('SELECT * FROM shop_variants WHERE product_id=%s GROUP BY size_id',[id])
            colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id)
            variant = Variants.objects.get(id=variants[0].id)
        context.update({
                        'sizes': sizes,
                        'variant': variant,
                        'colors': colors,
                        'images': images,
                        'query': query,
                        'product': product,
                        'cart_product_form': cart_product_form
                        })

    return render(request, 'shop/product/detail.html', context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('shop/product/variant.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)