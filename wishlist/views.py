from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import WishlistItem
from portfolio.models import Gig
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def index(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    wishlist_products = [
        item.content_object
        for item in wishlist_items
        if isinstance(item.content_object, Gig)
    ]
    paginator = Paginator(wishlist_products, 9)
    page = request.GET.get("page", 1)
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    return render(request, "wishlist/wishlist.html", {"gig_list": response})


@login_required
def toggle_item(request, product_id, style):
    product = get_object_or_404(Gig, id=product_id)
    content_type = ContentType.objects.get_for_model(Gig)
    wishlist_item, created = WishlistItem.objects.get_or_create(
        content_type=content_type, object_id=product.id, user=request.user
    )

    if created:
        action = "added"
    else:
        wishlist_item.delete()
        action = "removed"

    if request.headers.get("Hx-Request"):
        return render(
            request,
            f"wishlist/_button-{style}.html",
            {"product": product, "action": action},
            content_type="text/html",
        )

    return redirect("wishlist:index")
