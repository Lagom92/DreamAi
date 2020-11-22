from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('infer/', include('inferences.urls')),
    path('', include('accounts.urls')),
]
