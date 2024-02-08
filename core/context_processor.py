from core.models import CartOrderItems, Product, Category, Vendor, CartOrder, ProductImages, ProductReview, wishlist_model, Address
from django.db.models import Min, Max
from django.contrib import messages
from ast import Add




def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()

    min_max_price = Product.objects.aggregate(Min("vendor_price"), Max("vendor_price"))
    

    if request.user.is_authenticated:
        try:
            wishlist = wishlist_model.objects.filter(user=request.user)
        except:
            messages.warning(request, "You need to login before accessing your wishlist.")
            wishlist = 0
    else:
        wishlist = 0
    try:
        address = Address.objects.get(user=request.user)
    except:
       address = None

    
    
    return {
        'categories':categories,
        'address':address,
        'wishlist':wishlist,
        'vendors':vendors,
        'min_max_price':min_max_price,
    }