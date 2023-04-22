from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag(takes_context=True)
def wishlist_button(context, product, style):
    request = context["request"]
    user = request.user
    is_in_wishlist = (
        user.is_authenticated and product.wishlist_items.filter(user=user).exists()
    )

    return render_to_string(
        f"wishlist/_button-{style}.html",
        {
            "style": style,
            "product": product,
            "action": "added" if is_in_wishlist else "removed",
        },
        request=request,
    )
