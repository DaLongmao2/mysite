from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from read_statistics import views as v
from mysite import views

urlpatterns = [
    path('', views.home ,name='home'),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('blog/', include('blog.urls')),
    path('login/', views.login, name='login'),
    path('comment/', include('comment.urls')),
    path('like/', include('likes.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)