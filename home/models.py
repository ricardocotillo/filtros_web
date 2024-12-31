from wagtail.models import Page
from products.models import Producto


class HomePage(Page):
    def get_context(self, request, *args, **kwargs):
        ctx = super().get_context(request, *args, **kwargs)
        ctx['featured_products'] = Producto.objects.filter(destacado=True)[:10]
        ctx['promoted_products'] = Producto.objects.filter(promocion=True)[:10]
        return ctx


class AboutPage(Page):
    pass
