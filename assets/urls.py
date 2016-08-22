from django.conf.urls import include, url
from assets.views import *
urlpatterns = [
    url(r'^$', index),
    url(r'main$', main),
    url(r'assetdetail/(.*)/', asset_detailmodelform),
    url(r'server$', server),
    url(r'serverdetail/(.*)/$', server_detail),
    url(r'idc/(.*)', idc),
    url(r'yewu/(.*)', yewu),
    url(r'expired/(\d+)/$', expired),
]