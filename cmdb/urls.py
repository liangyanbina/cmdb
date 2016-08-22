from django.conf.urls import include, url
from django.contrib import admin
import assets
from assets.views import *
from assets import urls
import settings
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/asset_add', asset_add),
    url(r'^api/asset_cpu', asset_cpu),
    url(r'^api/asset_server', asset_server),
    url(r'^$', test),
    url(r'^cmdb',include(assets.urls)),
]
