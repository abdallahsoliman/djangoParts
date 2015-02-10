from django.conf.urls import patterns, include, url
from django.contrib import admin

from djangoParts.urls import Urls
from mainPage.views import MainPage

url_list = [
            "",
            url(r'^admin/', include(admin.site.urls)),
        ]

url_maker = Urls(url_list)
url_list = url_maker.make(MainPage)

urlpatterns = patterns(*url_list)
