from django.contrib import admin
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.post_list,name='post_list'),
    path('blog/<slug:category_id>/',views.post_list, name='post_list_by_category'),
    # path('blog/<slug:tag_slug>/',views.post_list_by_tag, name='post_list_by_tag'),
    path('blog/<id>/<slug>/', views.post_details, name='post_details'),
    path('likes/',views.like_post,name='like_post'),
    path('blog/search',views.search_post,name='search_post'),
]
