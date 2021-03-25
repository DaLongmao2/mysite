from django.urls import path
from blog import views


urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('blog_detail/<int:blog_pk>', views.blog_detail, name='blog_detail'),
    path('blog_with_type/<int:blog_type_pk>', views.blog_with_type, name='blog_with_type'),
    path('blogs_with_date/<int:year>/<int:month>', views.blogs_with_date, name='blogs_with_date'),
]
