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

    # login
    url(r'^login/$', auth_views.login,
        {'template_name': 'pages/login.html'}, name='login_url'),
    url(r'^logout/$', auth_views.logout,
        {'next_page': '/'}, name='logout_url'),
]
