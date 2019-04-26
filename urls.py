"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from user.views import UserViewSet
from about.views import AboutViewSet
from friend.views import FriendViewSet
from live2d.views import Live2dViewSet
from notice.views import NoticeViewSet
from summary.views import SummaryViewSet
from comment.views import CommentViewSet
from third_auth.views import ThirdAuthViewSet
from blog.views import CategoryViewSet, BlogViewSet, TagViewSet


router = DefaultRouter()

router.register(r'tags', TagViewSet)
router.register(r'blogs', BlogViewSet)
router.register(r'about', AboutViewSet)
router.register(r'live2d', Live2dViewSet)
router.register(r'notice', NoticeViewSet)
router.register(r'friends', FriendViewSet)
router.register(r'summarys', SummaryViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'categorys', CategoryViewSet)
router.register(r'user', UserViewSet, base_name='user')
router.register(r'oauth', ThirdAuthViewSet, base_name='oauth')

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path(r'doc/', include_docs_urls(title='Blog Api')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
