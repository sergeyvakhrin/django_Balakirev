from django.urls import path, re_path, register_converter

from . import views
from . import converters
from .views import show_category, show_tag_postlist

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<slug:cat_slug>/', show_category, name='category'),
    path('tag/<slug:tag_slug>/', show_tag_postlist, name='tag'),



    # path('cats/<int:cats_id>/', views.categories, name='cats_id'),
    # path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats'),
    # # re_path(r"^archive/(?P<year>[0-9]{4})/", views.archive),
    # path("archive/<year4:year>/", views.archive, name='archive'),
]