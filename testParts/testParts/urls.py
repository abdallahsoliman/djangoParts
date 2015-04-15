from django.conf.urls import patterns, include, url
from django.contrib import admin

from page.views import Page

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testParts.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns = Page().getUrls()
