from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from django.shortcuts import render
from django.db.models.query import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.views.generic import (
    ListView, DetailView, TemplateView,
    UpdateView, DeleteView,
)
from django.views import View
from .models import Producto, Marca, Modelo, ProductoModelo
from .filters import (
    ProductoFilterSet, ProductoRestFilterSet,
    ModeloRestFilterSet, MarcaRestFilterSet,
)
from .serializers import (
    ProductoSerializer, MarcaSerializer,
    ModeloSerializer, ProductoModeloSerializer,
)


class ProductSearchListView(ListView):
    template_name = 'products/search_results.html'
    queryset = Producto.objects.all()
    paginate_by = 5
    ordering = ('codigo',)

    def get_queryset(self) -> QuerySet[Producto]:
        qs = super().get_queryset()
        print(self.request.GET)
        filt = ProductoFilterSet(self.request.GET, qs)
        return filt.qs.distinct()


class LineView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        slug = kwargs.get('slug')
        return render(request, f'products/line_{slug}.html')


class ProductsView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        products = Producto.objects.order_by('codigo')
        filt = ProductoFilterSet(request.GET, products)
        paginator = Paginator(filt.qs.distinct(), 10)
        page = paginator.page(1)
        brands = Marca.objects.order_by('nombre')[:10]
        models = Modelo.objects.order_by('nombre')[:10]
        years = ProductoModelo.objects.values_list(
            'ano',
            flat=True
        ).order_by('ano')
        year_min = years.first()
        year_max = years.last()
        # lines = list(
        #     Producto.objects.values_list('tipo', flat=True).distinct()
        # )
        ctx = {
            'lines': [],
            'filters': filt.data,
            'products': ProductoSerializer(page.object_list, many=True).data,
            'next': '/productos/productos/?page=2'
            if page.has_next() else None,
            'brands': MarcaSerializer(brands, many=True).data,
            'models': ModeloSerializer(models, many=True).data,
            'year_min': year_min,
            'year_max': year_max,
        }
        return render(request, 'products/products.html', ctx)


class ProductView(DetailView):
    model = Producto
    template_name = 'products/product.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        producto_modelos = ctx['object'].producto_modelos.select_related(
            'modelo', 'modelo__marca',
        )
        ctx['producto_modelos'] = producto_modelos
        return ctx


class CartTemplateView(TemplateView):
    template_name = 'products/cart.html'


class CartUpdateView(UpdateView):
    def post(self, request: HttpRequest, *args, **kwargs):
        code = request.POST.get('code')
        count = int(request.POST.get('count', '1'))
        product = Producto.objects.get(code=code)
        cart: dict = request.session.get('cart', {})
        if cart.get(product.codigo):
            cart[product.codigo]['count'] += count
        else:
            cart[product.codigo] = {
                'pk': product.pk,
                'code': product.codigo,
                'count': count,
            }
        request.session['cart'] = cart
        request.session.save()
        return JsonResponse(cart)


class CartDeleteView(DeleteView):
    def delete(self, request: HttpRequest, *args, **kwargs):
        code = request.POST.get('code')
        product = Producto.objects.get(code=code)
        cart: dict = request.session.get('cart', {})
        if cart.get(product.codigo):
            cart.pop(product.codigo, None)
        request.session['cart'] = cart
        request.session.save()
        return HttpResponse()


class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Producto.objects.order_by('codigo').distinct()
    serializer_class = ProductoSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductoRestFilterSet


class MarcaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Marca.objects.order_by('nombre').distinct()
    serializer_class = MarcaSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MarcaRestFilterSet


class ModeloViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Modelo.objects.order_by('nombre').distinct()
    serializer_class = ModeloSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ModeloRestFilterSet


class ProductoModeloViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductoModelo.objects.order_by('id').distinct()
    serializer_class = ProductoModeloSerializer
