from rest_framework.routers import DefaultRouter
from django.urls import path, include
from store.views import ClienteView, ProdutoView, ItemCarrinhoView, CompraView

router = DefaultRouter()
router.register(r'clientes', ClienteView, basename='cliente')
router.register(r'produtos', ProdutoView, basename='produto')
router.register(r'itens_carrinho', ItemCarrinhoView, basename='item_carrinho')
router.register(r'compras', CompraView, basename='compra')

urlpatterns = [
    path('', include(router.urls)),
    path('produtos/aplicar_desconto', ProdutoView.as_view({'post': 'aplicar_desconto'})),
]
