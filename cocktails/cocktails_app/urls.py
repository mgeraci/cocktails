from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    # admin
    url(r'^admin/', admin.site.urls),

    # main pages
    url(r'^$', views.index, name='index_url'),
    url(r'^ingredients/(?P<slug>[^/]+)/$', views.ingredient_category, name='ingredient_category'),
    url(r'^ingredient/(?P<slug>[^/]+)/$', views.ingredient, name='ingredient_url'),
    url(r'^recipe/(?P<slug>[^/]+)/$', views.recipe, name='recipe_url'),
    url(r'^search/$', views.search, name='search_url'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
