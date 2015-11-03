from django.conf.urls import patterns, include, url
from blogapp import views

#from django.contrib import admin
#admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', views.index, name ='index' ),	
    url(r'^delete/', views.delete, name ='delete'),
    url(r'^api/(?P<img_id>\w+)/$',views.img_api, name = 'img_api'),
    url(r'^admin/', views.admin, name = 'admin'),
	url(r'^login/', views.login, name = 'login'),
	url(r'^register/', views.register, name = 'register'),
	url(r'^logout/', views.logout, name = 'logout'),
	url(r'^add_post/', views.add_post, name = 'add_post'),	
	url(r'^database_operation/', views.database_operation, name = 'database_operation')
)
