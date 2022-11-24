from django.shortcuts import render, redirect
from .models import Product_Table, Product_Category, size, Embroidery, CartItem, color, Cart
# Create your views here.
import uuid
from urllib import response
import urllib.request


def index(request):
    all_products = Product_Table.objects.filter(availability='Available')
    all_categories = Product_Category.objects.all()
    home = True
    context = {'all_products':all_products, 'all_categories':all_categories, 'home':home}
    return render(request, 'index.html', context)



def category_products(request, pk):
    get_cat = Product_Category.objects.get(id=pk) # specific category product getting from database
    all_products = Product_Table.objects.filter(availability='Available', Product_Category=get_cat)
    all_categories = Product_Category.objects.all()
    context = {'all_products':all_products, 'all_categories':all_categories, 'get_cat':get_cat}
    return render(request, 'index.html', context)



# product details page function
def product_details(request, pk):
    get_products = Product_Table.objects.get(id = pk) # specific product getting from database

    # this product has size variations
    if size.objects.filter(Product=get_products):
        # count range of lowest and highest price
        first_filter_sizes = size.objects.filter(Product=get_products).order_by('price').first()
        last_filter_sizes = size.objects.filter(Product=get_products).order_by('price').last()
        last_filter_Embroidery = Embroidery.objects.filter(Product=get_products).order_by('Additional_Price').last()
        first_price = 0
        last_price = 0
        if first_filter_sizes:
            first_price = first_filter_sizes.price
            if last_filter_Embroidery:
                last_price = last_filter_sizes.price + last_filter_Embroidery.Additional_Price
            else:
                last_price = last_filter_sizes.price
        price_range = True
    else:
        last_filter_Embroidery = Embroidery.objects.filter(Product=get_products).order_by('Additional_Price').last()
        price_product_table = get_products.Price
        first_price = price_product_table

        if last_filter_Embroidery:
            last_price = price_product_table + last_filter_Embroidery.Additional_Price
            price_range = True
        else:
            last_price = price_product_table
            price_range = False



    context = {'get_products':get_products, 'first_price':first_price, 'last_price':last_price, 'price_range':price_range}
    return render(request, 'product_details.html', context)


# add to cart to sesstion and save to database
def add_to_cart(request):
    id_prod = request.POST.get('id_prod')
    price_product = request.POST.get('price_product')

    get_color_by_id = None
    get_size_by_id = None
    get_embroidery_by_id = None
    price_var = price_product

    color_prod = request.POST.get('color_prod')
    if color_prod:
        ColorArray = color_prod.split(",")
        color_value = ColorArray[0]
        color_id = ColorArray[1]
        print(color_value, color_id)

        # get color table row
        get_color_by_id = color.objects.get(id=color_id)


    size_prod = request.POST.get('size_prod')
    if size_prod:
        SizeArray = size_prod.split(",")
        size_value = SizeArray[0]
        size_id = SizeArray[1]
        print(size_value, size_id)

        # get the row of size
        get_size_by_id = size.objects.get(id=size_id)
        price_var = get_size_by_id.price


    embroidery_prod = request.POST.get('embroidery_prod')
    print(embroidery_prod)
    print('embroidery_prod')
    if embroidery_prod:
        EmbroideryArray = embroidery_prod.split(",")
        Embroidery_value = EmbroideryArray[0]
        Embroidery_id = EmbroideryArray[1]
        print(Embroidery_id, Embroidery_value)
        print('Embroidery_id')

        if Embroidery_id == "0":
            get_embroidery_by_id = None
        else:
            get_embroidery_by_id = Embroidery.objects.get(id=Embroidery_id)
            price_var = int(price_var) + get_embroidery_by_id.Additional_Price

    print(id_prod, price_product, color_prod, size_prod, embroidery_prod)

    get_product_by_id = Product_Table.objects.get(id=id_prod)

    # setup session for identify uniqe anonymous user in add to cart table
    print(request.session.get('Anonymous_User_session_id'))
    if request.session.get('Anonymous_User_session_id'):
        Anonymous_User_session_id = request.session.get('Anonymous_User_session_id')
    else:
        uid_Anonymous_User_session_id = str(uuid.uuid1())
        request.session['Anonymous_User_session_id'] = uid_Anonymous_User_session_id
        Anonymous_User_session_id = request.session.get('Anonymous_User_session_id')

    qty = 1

    if Cart.objects.filter(Anonymous_User_session_id=Anonymous_User_session_id):
        my_cart = Cart.objects.get(Anonymous_User_session_id=Anonymous_User_session_id)
    else:
        my_cart = Cart(Anonymous_User_session_id=Anonymous_User_session_id, Total_Cart_Amount=0)
        my_cart.save()

    CartItem_setup = CartItem(Anonymous_User_session_id=my_cart, product=get_product_by_id, Color=get_color_by_id, Size=get_size_by_id, Embroidery=get_embroidery_by_id, quantity=qty, price=price_var, Subtotal_price=qty*int(price_var), is_active=True)
    CartItem_setup.save()

    update_addtocart(request, Anonymous_User_session_id)
    return redirect('product_details', id_prod)


def update_addtocart(request, Anonymous_User_session_id):
    my_cart = Cart.objects.get(Anonymous_User_session_id=Anonymous_User_session_id)

    filter_CartItem = CartItem.objects.filter(Anonymous_User_session_id=my_cart, is_active=True)
    # qty_CartItem_count = filter_CartItem.count()


    dict = {}
    lst = []
    total_price = 0
    qty_CartItem_count = 0

    for cart in filter_CartItem:

        # if cart has color variations
        if cart.Color:
            cart_color_id = cart.Color.id
            cart_color_color = cart.Color.color
        else:
            cart_color_id = 0
            cart_color_color = None

        if cart.Size:
            cart_size_id = cart.Size.id
            cart_size_size = cart.Size.size
        else:
            cart_size_id = 0
            cart_size_size = None

        if cart.Embroidery:
            id_Embroidery = cart.Embroidery.id
            name_Embroidery = cart.Embroidery.Embroidery
        else:
            id_Embroidery = 0
            name_Embroidery = None


        cart_prod_details = [cart.product.id, cart.product.Product_Name, cart.product.Product_Picture_upload_1.url]
        cart_color_details = [cart_color_id, cart_color_color]
        cart_size_details = [cart_size_id, cart_size_size]
        cart_embroidery_details = [id_Embroidery, name_Embroidery]

        subtotal = int(cart.price) * int(cart.quantity)

        qty_CartItem_count = qty_CartItem_count + int(cart.quantity)

        total_price = total_price + subtotal

        dict[cart.id] = cart.Anonymous_User_session_id.Anonymous_User_session_id, cart_prod_details, cart_color_details, cart_size_details, cart_embroidery_details, cart.quantity, cart.price, subtotal, cart.is_active

        str_ids = str(cart.product.id) + "_" + str(cart_color_id) + "_" + str(cart_size_id) + "_" + str(id_Embroidery)
        lst.append(str_ids)

        print(str_ids)

    my_cart.Total_Cart_Amount=total_price
    my_cart.save()

    request.session['list_of_items'] = lst

    request.session['CartTotal'] = dict

    request.session['total_qty'] = qty_CartItem_count

    request.session['total_price'] = total_price


# cart page
def cart(request):
    return render(request, 'cart.html')


# decrease item from cart cart page
def decrease_item(request):
    cart_item_id = request.POST.get('cart_item_id')
    print(cart_item_id)
    print(type(cart_item_id))
    getitem = CartItem.objects.get(id=cart_item_id)

    print(getitem)
    print(getitem.quantity)
    if getitem.quantity <= 1:
        getitem.delete()
    else:
        getitem.quantity = getitem.quantity - 1
        getitem.Subtotal_price = getitem.quantity * getitem.price
        getitem.save()

    update_addtocart(request, getitem.Anonymous_User_session_id)
    return redirect('cart')

# increase item from cart cart page
def increase_item(request):
    cart_item_id = request.POST.get('cart_item_id')

    getitem = CartItem.objects.get(id=cart_item_id)

    getitem.quantity = getitem.quantity + 1
    getitem.Subtotal_price = getitem.quantity * getitem.price
    getitem.save()

    update_addtocart(request, getitem.Anonymous_User_session_id)
    return redirect('cart')


# Delete item from cart cart page
def delete_item(request):
    cart_item_id = request.POST.get('cart_item_id')
    getitem = CartItem.objects.get(id=cart_item_id)
    getitem.is_active=False
    getitem.save()
    update_addtocart(request, getitem.Anonymous_User_session_id)
    return redirect('cart')