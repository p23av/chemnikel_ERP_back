from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, ContactPersonViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'contact-persons', ContactPersonViewSet)
router.register(r'products', ProductViewSet)

# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
]