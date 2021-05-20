from rest_framework.routers import DefaultRouter

from logistic.views import ProductViewSet, StockViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('stocks', StockViewSet, basename='stocks')

urlpatterns = router.urls
