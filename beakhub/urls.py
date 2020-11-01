from django.conf.urls import url
from beakhub import views

urlpatterns = (
    url(r'^accounts$', views.account_list),
    url(r'^accounts/(?P<id>[0-9]+)$', views.account_details),
    url(r'^accounts/login$', views.account_login),
    url(r'^users$', views.user_list),
    url(r'^users/(?P<id>[0-9]+)$', views.user_details),
    url(r'^categories$', views.category_list),
    url(r'^categories/(?P<id>[0-9]+)$', views.category_details),
    url(r'^jobs$', views.job_list),
    url(r'^jobs/(?P<id>[0-9]+)$', views.job_details),
    url(r'^jobs/user/(?P<user_id>[0-9]+)$', views.jobs_by_user),
    url(r'^address$', views.address_list),
    url(r'^address/(?P<id>[0-9]+)$', views.address_details),
    url(r'^address/job/(?P<job_id>[0-9]+)$', views.address_by_job),
)