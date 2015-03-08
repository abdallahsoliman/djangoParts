from django.conf.urls import patterns, include, url
from django.contrib import admin

from page.views import Page

"""
from index.views import Index
from inner.views import Inner
from info.views import Info
from index.views import IndexOptions
"""

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

)

urlpatterns = Page().getUrls(Page)
