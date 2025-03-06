from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ItemTypeViewSet,
    InventoryItemViewSet,
    LocationViewSet,
    ItemLocationAssignmentViewSet,
    ItemAssociationViewSet,
    UserRegisterView,
    LocationReportView,
    FullLocationReportView,
    InventoryExportView,
    InventoryStatsView,
    BulkTransferView,
    InventoryImportView  # импортируем наш новый класс
)
from rest_framework_simplejwt import views as jwt_views

router = DefaultRouter()
router.register(r'item-types', ItemTypeViewSet)
router.register(r'inventory-items', InventoryItemViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'item-location-assignments', ItemLocationAssignmentViewSet)
router.register(r'item-associations', ItemAssociationViewSet)

urlpatterns = [
    path('inventory-items/bulk-transfer/', BulkTransferView.as_view(), name='bulk_transfer'),
    path('', include(router.urls)),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('reports/locations/', LocationReportView.as_view(), name='location_report'),
    path('reports/locations/full/', FullLocationReportView.as_view(), name='location_full_report'),
    path('export/inventory/', InventoryExportView.as_view(), name='inventory_export'),
    path('reports/stats/', InventoryStatsView.as_view(), name='inventory_stats'),
    # Новый URL для импорта инвентаря из CSV
    path('import/inventory/', InventoryImportView.as_view(), name='inventory_import'),
]

