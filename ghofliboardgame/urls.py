"""ghofliboardgame URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from website import views
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^entercategory', views.enter_bgg_category),
    url(r'^entermech', views.enter_bgg_mechanics),
    url(r'^enterfamily', views.enter_bgg_family),
    url(r'^searchproduct', views.search),
    url(r'^enterbggitem', views.bgg_enter_items),
    url(r'^enterimages', views.save_image),
    url(r'^enterfiles', views.save_file),
    url(r'^entervideos', views.save_video),
    url(r'^enterexpansions', views.save_expansion),
    url(r'^enterforums', views.save_forum),
    url(r'^entercredits', views.save_credits),
    url(r'^signup', views.register),
    url(r'^login', views.login),
    url(r'^logout', views.logout),
    url(r'^getcuser', views.get_current_user),
    url(r'^getbglikes', views.get_bg_likes),
    url(r'^likebg', views.like_bg),
    url(r'^wishbg', views.wish_bg),
    url(r'^hasbg', views.has_bg),
    url(r'^ratebg', views.rate_bg),
    url(r'^profile', views.profile),
    url(r'^getuserbg', views.get_user_bg_data),
    url(r'^public/media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url('boardgame/(?P<bgg_code>\w{0,50})$', views.show_boardgame),
    url(r'^', views.index),
]
