from django.template import Library

register = Library()

@register.simple_tag

def cake_in_wishlist(request,uuid):

    if request.user and request.user.is_authenticated and request.user.role == 'User':

        return request.user.wishlist.cakes.filter(uuid=uuid).exists()