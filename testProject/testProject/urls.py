from django.conf.urls import patterns, include, url
from django.contrib import admin

from page.views import Page
from index.views import Index
from inner.views import Inner
from info.views import Info

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r"^$", Page.as_view(), name=Page.NAME),
    url(r"^page_container", Page.PAGE_CONTAINER.as_view(), name=Page.PAGE_CONTAINER.NAME),
    url(r"^index$", Index.as_view(), name=Index.NAME),
    url(r"^inner$", Inner.as_view(), name=Inner.NAME),
    url(r"^info$", Info.as_view(), name=Info.NAME),
)

urlpatters = Page().getUrls()
