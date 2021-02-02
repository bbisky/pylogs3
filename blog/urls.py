from django.urls import path, re_path
from django.contrib.syndication.views import Feed
from . import views
from . import feeds
from blog.models import Post
# Info for feeds.
# feed_dict = {    
#     'rss': feeds.RssLatestPosts,
#     'atom': feeds.AtomLatestPosts,
#     }
# info_dict = {    
#     'queryset': Post.objects.all(),
#     'date_field': 'pubdate',
# }

urlpatterns = [
    path('', views.index, name='index'),
    #tags
    path(r'tags/',views.tags,name='tags'),
    re_path(r'^tags/(?P<tagname>.*)/$',views.tags,name='tagname'),                        
    re_path(r'^(\d{4})/(\d{1,2})/(\d{1,2})/(?P<postname>[^/]+)/$',views.post,name='post_name'),
    #ajax
    re_path(r'^post/(?P<postid>(\d+))/comment$',views.post_comment,name='post_comment'),
    #url(r'^post/(?P<postid>(\d+))/comments', 'get_post_comments', name='ajax_post_comments'),
    #category view
    re_path(r'^category/(?P<catid>\d+)/$',views.categoryView,name="category_id"),
    re_path(r'^category/(?P<catname>[^/]+)/$',views.categoryView,name="category_name"),                        
    re_path(r'^(?P<year>\d{4})/(?P<month>(\d{1,2})?)/?(?P<date>(\d{1,2})?)/?$',views.dateposts),
    re_path(r'^(?P<pagename>\w+)/$',views.page,name='page'),
    re_path(r'^(.+?)(?P<pagename>\w+)/$',views.page,name='page'),   
    path('feeds/rss/', feeds.RssLatestPosts(), name='rss'),
    path('feeds/atom/', feeds.AtomLatestPosts(), name='atom'),
    #re_path(r'^feeds/(?P<url>\w+)/$',Feed, {'feed_dict':feed_dict},name='feeds'),
    #path(r'^rpc/$',blog.rpc.call,name='rpc'),
]