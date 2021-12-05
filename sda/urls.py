from django.contrib import admin
from django.urls import path
from manifest.views import manifest, skydiver_detail, unassigned_requests_list, lifts_list, vue, bind_request_to_lift
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('', vue),
    path('manifest/skydivers', manifest),
    path('skydiver/<int:id>/', skydiver_detail, name = "skydiver_detail"),
    path('manifest/request/json', unassigned_requests_list),
    path('manifest/lift/json', lifts_list),
    path('bind_request_to_lift/', bind_request_to_lift)
]