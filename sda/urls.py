from django.contrib import admin
from django.urls import path
from manifest.views import manifest, skydiver_detail, unassigned_requests_list, lifts_list, vue, bind_request_to_lift, SkydiverRequestViewSet, SkydiveDisciplineViewSet
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'skydiverrequest', SkydiverRequestViewSet)
router.register(r'skydivediscipline', SkydiveDisciplineViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('', manifest),
    path('manifest/skydivers', manifest),
    path('skydiver/<int:id>/', skydiver_detail, name = "skydiver_detail"),
    path('manifest/request/json', unassigned_requests_list),
    path('manifest/lift/json', lifts_list),
    path('bind_request_to_lift/', bind_request_to_lift)
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)