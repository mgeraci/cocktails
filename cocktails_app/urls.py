from django.conf.urls import re_path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    # admin
    re_path(r'^admin/', admin.site.urls),

    # main pages
    re_path(r'^$', views.index, name='index_url'),

    re_path(r'^ingredients/$', views.ingredients, name='ingredients_url'),
    re_path(r'^sources/$', views.sources, name='sources_url'),
    re_path(r'^recipes/$', views.recipes, name='recipes_url'),
    re_path(r'^search/$', views.search, name='search_url'),

    # individual pages
    re_path(r'^ingredient/(?P<slug>[^/]+)/$', views.ingredient, name='ingredient_url'),
    re_path(r'^source/(?P<slug>[^/]+)/$', views.source, name='source_url'),
    re_path(r'^recipe/(?P<slug>[^/]+)/$', views.recipe, name='recipe_url'),
    re_path(r'^recipe/l/(?P<slug>[^/]+)/$', views.recipe_share, name='recipe_share_url'),

    # authentication
    re_path(r'^api_login/$', views.api_login, name='api_login_url'),
    re_path(r'^login/$', views.site_login, name='login_url'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(),
        {'next_page': '/'}, name='logout_url'),

    # ios app
    re_path(r'^apple-app-site-association', views.apple_app_site_association),
]
