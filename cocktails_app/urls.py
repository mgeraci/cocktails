from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    # admin
    url(r'^admin/', admin.site.urls),

    # main pages
    url(r'^$', views.index, name='index_url'),

    url(r'^ingredients/$', views.ingredients, name='ingredients_url'),
    url(r'^sources/$', views.sources, name='sources_url'),
    url(r'^recipes/$', views.recipes, name='recipes_url'),
    url(r'^search/$', views.search, name='search_url'),

    # individual pages
    url(r'^ingredient/(?P<slug>[^/]+)/$', views.ingredient, name='ingredient_url'),
    url(r'^source/(?P<slug>[^/]+)/$', views.source, name='source_url'),
    url(r'^recipe/(?P<slug>[^/]+)/$', views.recipe, name='recipe_url'),
    url(r'^recipe/l/(?P<slug>[^/]+)/$', views.recipe_share, name='recipe_share_url'),

    # authentication
    url(r'^api_login/$', views.api_login, name='api_login_url'),
    url(r'^login/$', views.site_login, name='login_url'),
    url(r'^logout/$', auth_views.LogoutView.as_view(),
        {'next_page': '/'}, name='logout_url'),

    # ios app
    url(r'^apple-app-site-association', views.apple_app_site_association),
]
