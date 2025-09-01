from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('iamadmin/', admin.site.urls),

    # App URLs
    path('contact/', include('apps.contact.urls')),
    path('', include(('apps.core.urls', 'core'), namespace='core')),
    path('blog/', include(('apps.blog.urls', 'blog'), namespace='blog')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),

    # ✅ Media files (works for DEBUG=False too)
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# ✅ Static files (Django will serve in DEBUG=True; in production collectstatic should be used)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
