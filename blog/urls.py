from django.contrib import admin
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.post_list,name='post_list'),
    path('blog/<id>/<slug>/', views.post_details, name='post_details'),
]
