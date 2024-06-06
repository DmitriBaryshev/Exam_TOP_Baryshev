from django.urls import path, re_path, register_converter
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.add_blog, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_p, name='login_p'),
    path('register/', views.register, name='register'),
    path('post/<int:post_id>/', views.show_post, name='post'),
    path('category/<int:cat_id>/', views.show_category, name='category'),
    # path('cat/<slug:cat_slug>/', views.categories_by_slug, name='cats'),
]
