from django.contrib import admin
from django.urls import path
from manifest.views import PlaneLiftViewSet, manifest, skydiver_detail, bind_request_to_lift, SkydiverRequestViewSet, SkydiveDisciplineViewSet
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'request', SkydiverRequestViewSet)
router.register(r'discipline', SkydiveDisciplineViewSet)
router.register(r'lift', PlaneLiftViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('', manifest),
    path('manifest/skydivers', manifest),
    path('skydiver/<int:id>/', skydiver_detail, name = "skydiver_detail"),
    path('bind_request_to_lift/', bind_request_to_lift)
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)