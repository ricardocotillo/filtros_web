from rest_framework import routers
from django.urls import path
from .views import (
    ProductSearchListView, ProductsView,
    ProductView, CartTemplateView, CartUpdateView,
    CartDeleteView, ProductoViewSet, MarcaViewSet,
    ModeloViewSet, ProductoModeloViewSet,
)

app_name = 'products'

router = routers.SimpleRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'modelos', ModeloViewSet)
router.register(r'producto-modelo', ProductoModeloViewSet)

urlpatterns = [
    path('search/', ProductSearchListView.as_view(), name='search',),
    path('cart/', CartTemplateView.as_view(), name='cart'),
    path('cart/update/', CartUpdateView.as_view(), name='cart-update'),
    path('cart/delete/', CartDeleteView.as_view(), name='cart-delete'),
    path('<int:pk>/', ProductView.as_view(), name='product'),
    path('', ProductsView.as_view(), name='products',),
] + router.urls
